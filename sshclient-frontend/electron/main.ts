import { app, BrowserWindow, BrowserView, globalShortcut } from 'electron'
import path from 'node:path'
// const electron = require('electron')

// The built directory structure
//
// ├─┬─┬ dist
// │ │ └── index.html
// │ │
// │ ├─┬ dist-electron
// │ │ ├── main.js
// │ │ └── preload.js
// │
process.env.DIST = path.join(__dirname, '../dist')
process.env.PUBLIC = app.isPackaged ? process.env.DIST : path.join(process.env.DIST, '../public')


let win: BrowserWindow | null
// 🚧 Use ['ENV_NAME'] avoid vite:define plugin - Vite@2.x
const VITE_DEV_SERVER_URL = process.env['VITE_DEV_SERVER_URL']

function createWindow() {
  // const Menu = electron.Menu
  // Menu.setApplicationMenu(null)
  win = new BrowserWindow({
    icon: path.join(process.env.PUBLIC, 'electron-vite.svg'),
    webPreferences: {
      preload: path.join(__dirname, 'preload.js'),
    },
    // titleBarStyle: 'hidden'
  })
  win.removeMenu()
  globalShortcut.register('CommandOrControl+Shift+i', function () {
    win.webContents.openDevTools()
  })

//   const view = new BrowserView()
// win.setBrowserView(view)
// view.setBounds({ x: 0, y: 0, width: 300, height: 300 })
// view.webContents.loadURL('https://electronjs.org')

  // Test active push message to Renderer-process.
  win.webContents.on('did-finish-load', () => {
    win?.webContents.send('main-process-message', (new Date).toLocaleString())
  })

  if (VITE_DEV_SERVER_URL) {
    win.loadURL(VITE_DEV_SERVER_URL)
  } else {
    // win.loadFile('dist/index.html')
    win.loadFile(path.join(process.env.DIST, 'index.html'))
  }
}

app.on('window-all-closed', () => {
  win = null
})

//在ready事件里
// app.on('ready', async () => {
//   globalShortcut.register('F12', function () {
//     win.webContents.openDevTools()
//   })
//   createWindow();
// })


app.whenReady().then(createWindow)
