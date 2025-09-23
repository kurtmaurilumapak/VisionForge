const { app, BrowserWindow, Menu, dialog } = require('electron');
const path = require('path');
const { spawn } = require('child_process');
const isDev = process.env.NODE_ENV === 'development';

let mainWindow;
let backendProcess;
let shutdownWatchdogInterval = null;

async function startBackend() {
  console.log('Starting backend server...');

  const backendPath = path.join(__dirname, '../backend');
  const isProduction = !isDev;
  const fs = require('fs');
  const { app: electronApp } = require('electron');
  const logsDir = path.join(electronApp.getPath('userData'), 'logs');
  try { if (!fs.existsSync(logsDir)) fs.mkdirSync(logsDir, { recursive: true }); } catch (_) {}
  const logFile = path.join(logsDir, `backend-${Date.now()}.log`);
  const logStream = fs.createWriteStream(logFile, { flags: 'a' });
  
  // In production, prefer launching the bundled backend executable
  if (isProduction) {
    try {
      const exeName = process.platform === 'win32' ? 'visionforge_backend.exe' : 'visionforge_backend';
      const bundledPath = path.join(process.resourcesPath, 'backend', exeName);
      if (fs.existsSync(bundledPath)) {
        backendProcess = spawn(bundledPath, [], {
          cwd: path.dirname(bundledPath),
          stdio: 'pipe',
          shell: false,
          env: {
            ...process.env,
            ELECTRON: '1',
            RELOAD: 'false'
          }
        });

        backendProcess.stdout.on('data', (data) => { console.log(`Backend: ${data}`); try { logStream.write(data); } catch (_) {} });
        backendProcess.stderr.on('data', (data) => { console.error(`Backend Error: ${data}`); try { logStream.write(data); } catch (_) {} });
        backendProcess.on('close', (code) => console.log(`Backend process exited with code ${code}`));
        backendProcess.on('error', (err) => console.error('Failed to start bundled backend:', err));

        return; // done
      }
    } catch (e) {
      console.error('Error checking bundled backend:', e);
    }
  }

  // Determine python command per platform
  let pythonCommand = 'python';
  if (process.platform !== 'win32') {
    pythonCommand = 'python3';
  }

  // On Windows prefer the launcher if available
  const tryCommands = process.platform === 'win32'
    ? [ ['py', ['-3']], ['python', []] ]
    : [ ['python3', []], ['python', []] ];

  function spawnCheck(cmd, args) {
    return new Promise((resolve) => {
      const p = spawn(cmd, [...args, '--version'], { shell: false });
      p.on('error', () => resolve(false));
      p.on('exit', (code) => resolve(code === 0));
    });
  }

  for (const [cmd, args] of tryCommands) {
    // eslint-disable-next-line no-await-in-loop
    const ok = await spawnCheck(cmd, args);
    if (ok) { pythonCommand = cmd; break; }
  }

  // Prefer running start.py which configures uvicorn
  const script = path.join(backendPath, 'start.py');
  const args = [script];

  backendProcess = spawn(pythonCommand, args, {
    cwd: backendPath,
    stdio: 'pipe',
    shell: false,
    env: {
      ...process.env,
      ELECTRON: '1',
      RELOAD: 'false'
    }
  });

  backendProcess.stdout.on('data', (data) => { console.log(`Backend: ${data}`); try { logStream.write(data); } catch (_) {} });

  backendProcess.stderr.on('data', (data) => { console.error(`Backend Error: ${data}`); try { logStream.write(data); } catch (_) {} });

  backendProcess.on('close', (code) => {
    console.log(`Backend process exited with code ${code}`);
  });

  backendProcess.on('error', (err) => {
    console.error('Failed to start backend:', err);
  });

  // If backend exits quickly with error, try installing dependencies once and retry
  return new Promise((resolve) => {
    let exited = false;
    const earlyExitTimer = setTimeout(() => {
      if (!exited) resolve();
    }, 3000);

    backendProcess.once('close', async (code) => {
      exited = true;
      clearTimeout(earlyExitTimer);
      if (code === 0) {
        resolve();
        return;
      }
      console.log('Backend exited early; attempting to install Python deps and retry...');
      try {
        await ensureBackendDependencies(backendPath, pythonCommand);
      } catch (e) {
        console.error('Dependency installation failed:', e);
      }

      // Retry once
      backendProcess = spawn(pythonCommand, args, {
        cwd: backendPath,
        stdio: 'pipe',
        shell: false,
        env: {
          ...process.env,
          ELECTRON: '1',
          RELOAD: 'false'
        }
      });
      backendProcess.stdout.on('data', (data) => { console.log(`Backend: ${data}`); try { logStream.write(data); } catch (_) {} });
      backendProcess.stderr.on('data', (data) => { console.error(`Backend Error: ${data}`); try { logStream.write(data); } catch (_) {} });
      backendProcess.once('close', (code2) => {
        console.log(`Backend retry exited with code ${code2}`);
        resolve();
      });
    });
  });
}

async function waitForBackendReady(timeoutMs = 15000) {
  const started = Date.now();
  const url = 'http://localhost:8000/health';
  while (Date.now() - started < timeoutMs) {
    try {
      // Node 18+ has global fetch
      const res = await fetch(url, { method: 'GET' });
      if (res.ok) {
        return true;
      }
    } catch (_) {
      // ignore until ready
    }
    // wait 300ms between attempts
    // eslint-disable-next-line no-await-in-loop
    await new Promise((r) => setTimeout(r, 300));
  }
  return false;
}

function ensureBackendDependencies(backendPath, pythonCmd) {
  return new Promise((resolve, reject) => {
    console.log('Installing backend dependencies...');
    const pipArgs = ['-m', 'pip', 'install', '-r', 'requirements.txt'];
    const installer = spawn(pythonCmd, pipArgs, { cwd: backendPath, shell: false });
    installer.stdout.on('data', (d) => console.log(`pip: ${d}`));
    installer.stderr.on('data', (d) => console.error(`pip error: ${d}`));
    installer.on('close', (code) => {
      if (code === 0) resolve(); else reject(new Error(`pip exited with ${code}`));
    });
    installer.on('error', (err) => reject(err));
  });
}

function stopBackend() {
  console.log('Stopping backend server...');

  const pid = backendProcess && backendProcess.pid;

  function forceKill() {
    try {
      if (process.platform === 'win32') {
        // Kill process tree on Windows
        const { spawn } = require('child_process');
        spawn('taskkill', ['/PID', String(pid), '/T', '/F']);
      } else {
        process.kill(pid, 'SIGKILL');
      }
    } catch (_) {
      // ignore
    }
  }

  if (pid) {
    try {
      if (process.platform === 'win32') {
        // SIGTERM is not well supported on Windows python, try default kill
        backendProcess.kill();
      } else {
        // Graceful first
        process.kill(pid, 'SIGTERM');
      }
    } catch (_) {
      // fallback
      forceKill();
    }

    // Fallback force kill after 2s if still alive
    setTimeout(() => {
      try {
        process.kill(pid, 0); // check alive
        forceKill();
      } catch (_) {
        // already dead
      }
    }, 2000);
  }

  // Ultimate safety on Windows: kill by image name, in case PID tracking failed
  if (process.platform === 'win32') {
    try {
      const { spawn } = require('child_process');
      spawn('taskkill', ['/IM', 'visionforge_backend.exe', '/T', '/F']);
    } catch (_) {}
  }

  backendProcess = null;
}

function createWindow() {
  // Create the browser window
  mainWindow = new BrowserWindow({
    width: 1200,
    height: 800,
    minWidth: 800,
    minHeight: 600,
    title: '',
    webPreferences: {
      nodeIntegration: false,
      contextIsolation: true,
      enableRemoteModule: false,
      preload: path.join(__dirname, 'preload.js')
    },
    icon: path.join(__dirname, '../src/assets/visionforge_logo.ico'),
    iconSize: 256,
    titleBarStyle: 'default',
    show: false,
    autoHideMenuBar: true
  });

  // Load the app
  if (isDev) {
    mainWindow.loadURL('http://localhost:5173');
    // Comment out dev tools to prevent unwanted tabs
    // mainWindow.webContents.openDevTools();
  } else {
    mainWindow.loadFile(path.join(__dirname, '../dist/index.html'));
  }

  // Show window when ready to prevent visual flash
  mainWindow.once('ready-to-show', () => {
    mainWindow.show();
  });

  // Handle window closed
  mainWindow.on('closed', () => {
    mainWindow = null;
  });
}

// This method will be called when Electron has finished initialization
app.whenReady().then(() => {
  // Start backend server first, then wait until it's ready
  startBackend()
    .then(() => waitForBackendReady())
    .then((ready) => {
      if (!ready) {
        const logPath = path.join(require('electron').app.getPath('userData'), 'logs');
        console.error('Backend did not become ready in time.');
        dialog.showErrorBox('Backend failed to start', `The VisionForge backend did not start.

Please share the latest log file from:\n${logPath}\n\nThe app UI will still open, but processing will not work until the backend is running.`);
      }
    })
    .finally(() => {
      createWindow();
      // Start watchdog to ensure backend is killed when app has no windows
      if (process.platform === 'win32') {
        if (shutdownWatchdogInterval) clearInterval(shutdownWatchdogInterval);
        shutdownWatchdogInterval = setInterval(() => {
          try {
            if (BrowserWindow.getAllWindows().length === 0) {
              const { spawn } = require('child_process');
              spawn('taskkill', ['/IM', 'visionforge_backend.exe', '/T', '/F']);
            }
          } catch (_) {}
        }, 1500);
      }
    });

  // On macOS, re-create window when dock icon is clicked
  app.on('activate', () => {
    if (BrowserWindow.getAllWindows().length === 0) {
      createWindow();
    }
  });
});

// Quit when all windows are closed
app.on('window-all-closed', () => {
  // On macOS, keep app running even when all windows are closed
  if (process.platform !== 'darwin') {
    stopBackend();
    app.quit();
  }
});

// Stop backend when app is about to quit
app.on('before-quit', () => {
  stopBackend();
});

// Extra hook just before quitting begins
app.on('will-quit', () => {
  stopBackend();
});

// Extra safety: stop backend on quit and exit events
app.on('quit', () => {
  stopBackend();
});
process.on('exit', () => {
  stopBackend();
});
process.on('SIGINT', () => {
  stopBackend();
  process.exit(0);
});
process.on('SIGTERM', () => {
  stopBackend();
  process.exit(0);
});

// Security: Prevent new window creation and external navigation
app.on('web-contents-created', (event, contents) => {
  contents.on('new-window', (event, navigationUrl) => {
    event.preventDefault();
  });
  
  contents.on('will-navigate', (event, navigationUrl) => {
    const parsedUrl = new URL(navigationUrl);
    if (parsedUrl.origin !== 'http://localhost:5173' && parsedUrl.origin !== 'file://') {
      event.preventDefault();
    }
  });
});

// Remove menu bar completely
Menu.setApplicationMenu(null);
