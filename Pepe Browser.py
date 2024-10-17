import sys
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QTabWidget, QVBoxLayout,
    QWidget, QToolBar, QAction, QMessageBox, QFileDialog, QLineEdit
)
from PyQt5.QtWebEngineWidgets import QWebEngineView
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import QUrl, QFileInfo

class BrowserTab(QWidget):
    def __init__(self):
        super().__init__()
        self.layout = QVBoxLayout(self)
        self.browser = QWebEngineView()
        self.layout.addWidget(self.browser)
        self.browser.setUrl(QUrl("http://glidebrowserproject.rf.gd/pesquisar.html"))  # Começa com Pepe Search

        # Conecta o evento de download
        self.browser.page().profile().downloadRequested.connect(self.on_download_requested)

    def on_download_requested(self, download):
        # Sugere um nome para o arquivo baseado na URL
        suggested_filename = download.url().fileName()
        download_path, _ = QFileDialog.getSaveFileName(self, "Salvar arquivo", suggested_filename, "Todos os Arquivos (*)")
        if download_path:
            download.setPath(download_path)
            download.accept()
            self.download_in_progress(download)

    def download_in_progress(self, download):
        # Mostra uma mensagem quando o download começa
        download.finished.connect(lambda: self.on_download_finished(download))
        QMessageBox.information(self, "Download Iniciado", f"Download iniciado: {QFileInfo(download.path()).fileName()}")

    def on_download_finished(self, download):
        # Informa quando o download é concluído
        QMessageBox.information(self, "Download Completo", f"Download concluído: {QFileInfo(download.path()).fileName()}")

class GlideBrowser(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Glide Browser")
        self.setGeometry(300, 100, 1200, 800)

        # Define o ícone do navegador
        self.setWindowIcon(QIcon("icon.ico"))  # Certifique-se de que o arquivo icon.ico está no diretório correto

        self.tabs = QTabWidget()
        self.tabs.setTabsClosable(True)  # Permite fechar abas
        self.tabs.tabCloseRequested.connect(self.close_current_tab)

        self.setCentralWidget(self.tabs)
        self.add_new_tab()  # Adiciona uma aba padrão na inicialização

        self.create_toolbar()

    def create_toolbar(self):
        toolbar = QToolBar()
        self.addToolBar(toolbar)

        # Botões de navegação
        back_action = QAction("Voltar", self)
        back_action.triggered.connect(self.back)
        toolbar.addAction(back_action)

        forward_action = QAction("Avançar", self)
        forward_action.triggered.connect(self.forward)
        toolbar.addAction(forward_action)

        reload_action = QAction("Recarregar", self)
        reload_action.triggered.connect(self.reload)
        toolbar.addAction(reload_action)

        # Campo para digitar URLs
        self.url_bar = QLineEdit()
        self.url_bar.returnPressed.connect(self.navigate_to_url)
        toolbar.addWidget(self.url_bar)

        # Botão para nova aba
        new_tab_action = QAction("Nova Aba", self)
        new_tab_action.triggered.connect(self.add_new_tab)
        toolbar.addAction(new_tab_action)

    def back(self):
        current_tab = self.tabs.currentWidget()
        if current_tab.browser.history().canGoBack():
            current_tab.browser.history().back()

    def forward(self):
        current_tab = self.tabs.currentWidget()
        if current_tab.browser.history().canGoForward():
            current_tab.browser.history().forward()

    def reload(self):
        current_tab = self.tabs.currentWidget()
        current_tab.browser.reload()

    def navigate_to_url(self):
        current_tab = self.tabs.currentWidget()
        url = self.url_bar.text()
        # Adiciona o prefixo http:// se a URL não começar com http/https
        if not url.startswith("http://") and not url.startswith("https://"):
            url = "http://" + url
        current_tab.browser.setUrl(QUrl(url))

    def add_new_tab(self):
        new_tab = BrowserTab()
        index = self.tabs.addTab(new_tab, "Nova Aba")
        self.tabs.setCurrentIndex(index)
        new_tab.browser.urlChanged.connect(self.update_url_bar)

    def update_url_bar(self, q):
        self.url_bar.setText(q.toString())

    def close_current_tab(self, index):
        if self.tabs.count() > 1:
            # Para qualquer reprodução e remove a aba atual
            current_tab = self.tabs.widget(index)
            current_tab.browser.setUrl(QUrl("about:blank"))  # Para qualquer reprodução
            self.tabs.removeTab(index)
        else:
            QMessageBox.warning(self, "Atenção", "Não é possível fechar a última aba.")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = GlideBrowser()
    window.show()
    sys.exit(app.exec_())
