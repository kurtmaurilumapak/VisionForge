const { contextBridge, ipcRenderer } = require('electron');

// Expose protected methods that allow the renderer process to use
// the ipcRenderer without exposing the entire object
contextBridge.exposeInMainWorld('electronAPI', {
  openFile: (callback) => {
    ipcRenderer.on('open-file', callback);
  },
  removeOpenFileListener: (callback) => {
    ipcRenderer.removeListener('open-file', callback);
  }
});
