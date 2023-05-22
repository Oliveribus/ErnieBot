# ErnieBot

## Anleitung zur Installation und Ausführung

**Voraussetzungen:**

Stellen Sie sicher, dass Sie Python und `pip` auf Ihrem Computer installiert haben. Sie können diese über die offizielle Python-Website herunterladen und installieren: https://www.python.org/downloads/

**Schritte zur Installation:**

1. **Klonen Sie das Repository:** Öffnen Sie ein Terminalfenster (auf MacOS oder Linux) oder eine Eingabeaufforderung (auf Windows) und navigieren Sie zu dem Ordner, in dem Sie das Projekt speichern möchten.

    ```
    git clone https://github.com/Oliveribus/ErnieBot.git
    ```


2. **Wechseln Sie in das Projektverzeichnis:** Wechseln Sie in das Verzeichnis, das durch das Klonen des Repositories erstellt wurde:

    ```
    cd ErnieBot
    ```


3. **Installieren Sie die benötigten Python-Bibliotheken:** Führen Sie den folgenden Befehl aus, um die Python-Bibliotheken zu installieren, die Ihr Projekt benötigt:

    ```
    pip install -r requirements.txt
    ```

4. **Installieren Sie das Paket:** Führen Sie den folgenden Befehl aus, um Ihr Python-Paket zu installieren:

    ```
    python setup.py install
    ```
5. Setzen Sie Ihren API Key in key.txt mit einem beliebigen Texteditor oder mit diesem Befehl.
Ersetzen Sie dabei YOURAPIKEY durch Ihren OpenAI API-Key ohne Anführungszeichen.
   ```
   echo YOURAPIKEY > key.txt
   ```
**Schritte zur Ausführung des Projekts:**

Führen Sie folgenden Befehl aus
```
python main.py
```


