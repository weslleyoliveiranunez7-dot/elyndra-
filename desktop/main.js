const { app, BrowserWindow, Menu } = require('electron');
const path = require('path');
app.commandLine.appendSwitch('autoplay-policy', 'no-user-gesture-required');
function pagina() {
  return app.isPackaged
    ? path.join(process.resourcesPath, 'www', 'index.html')
    : path.join(__dirname, '..', 'www', 'index.html');
}
function criar() {
  Menu.setApplicationMenu(null);
  const w = new BrowserWindow({
    width: 1280, height: 720, useContentSize: true, backgroundColor: '#000000',
    title: 'ELYNDRA', autoHideMenuBar: true,
    webPreferences: { contextIsolation: true, nodeIntegration: false, autoplayPolicy: 'no-user-gesture-required' }
  });
  w.loadFile(pagina());
  w.webContents.on('before-input-event', (e, i) => {
    if (i.type === 'keyDown' && i.key === 'F11') { w.setFullScreen(!w.isFullScreen()); e.preventDefault(); }
  });
}
app.whenReady().then(criar);
app.on('window-all-closed', () => app.quit());
                     
