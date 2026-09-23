// Exporta cada .pagina de un HTML a PDF (una página por archivo) y,
// opcionalmente, a PNG. Uso:
//   swift exportar.swift <html> <ancho> <alto> <carpeta-salida> [png]
import Cocoa
import WebKit

let args = CommandLine.arguments
let htmlURL = URL(fileURLWithPath: args[1])
let pageW = CGFloat(Double(args[2])!)
let pageH = CGFloat(Double(args[3])!)
let outDir = URL(fileURLWithPath: args[4], isDirectory: true)
let wantPNG = args.count > 5 && args[5] == "png"

final class Exporter: NSObject, WKNavigationDelegate {
  let web: WKWebView
  var pages = 0
  init(_ web: WKWebView) { self.web = web }

  func webView(_ webView: WKWebView, didFinish navigation: WKNavigation!) {
    // Carga y decodifica todas las imágenes (WebKit difiere las que están fuera de vista).
    webView.frame = NSRect(x: 0, y: 0, width: pageW, height: pageH * 40)
    let listo = "Promise.all([document.fonts.ready, ...[...document.images].map(i => { i.loading = 'eager'; return i.decode().catch(() => null); })]).then(() => 1)"
    webView.callAsyncJavaScript("return await (" + listo + ")", arguments: [:], in: nil, in: .page) { _ in
      DispatchQueue.main.asyncAfter(deadline: .now() + 2.0) {
        webView.evaluateJavaScript("document.querySelectorAll('.pagina').length") { n, _ in
          self.pages = (n as? Int) ?? 0
          webView.frame = NSRect(x: 0, y: 0, width: pageW, height: pageH * CGFloat(self.pages))
          // Una captura completa obliga a WebKit a pintar todas las imágenes antes del PDF.
          DispatchQueue.main.asyncAfter(deadline: .now() + 1.0) {
            webView.takeSnapshot(with: nil) { _, _ in
              DispatchQueue.main.asyncAfter(deadline: .now() + 1.5) { self.export(0) }
            }
          }
        }
      }
    }
  }

  func export(_ i: Int) {
    if i >= pages { print("paginas \(pages)"); exit(0) }
    let rect = CGRect(x: 0, y: pageH * CGFloat(i), width: pageW, height: pageH)
    let cfg = WKPDFConfiguration()
    cfg.rect = rect
    web.createPDF(configuration: cfg) { result in
      if case .success(let data) = result {
        try? data.write(to: outDir.appendingPathComponent(String(format: "p%02d.pdf", i + 1)))
      } else { print("error pdf \(i + 1)"); exit(1) }
      guard wantPNG else { self.export(i + 1); return }
      let snap = WKSnapshotConfiguration()
      snap.rect = rect
      snap.snapshotWidth = NSNumber(value: Double(pageW))
      self.web.takeSnapshot(with: snap) { image, _ in
        if let image = image, let tiff = image.tiffRepresentation,
           let rep = NSBitmapImageRep(data: tiff),
           let png = rep.representation(using: .png, properties: [:]) {
          try? png.write(to: outDir.appendingPathComponent(String(format: "p%02d.png", i + 1)))
        }
        self.export(i + 1)
      }
    }
  }
}

let app = NSApplication.shared
let web = WKWebView(frame: NSRect(x: 0, y: 0, width: pageW, height: pageH))
let window = NSWindow(contentRect: web.frame, styleMask: [.borderless], backing: .buffered, defer: false)
window.contentView = web
let exporter = Exporter(web)
web.navigationDelegate = exporter
web.loadFileURL(htmlURL, allowingReadAccessTo: htmlURL.deletingLastPathComponent().deletingLastPathComponent().deletingLastPathComponent())
DispatchQueue.main.asyncAfter(deadline: .now() + 120) { print("tiempo agotado"); exit(1) }
app.run()
