// Загружаем библиотеку Wi-Fi
#include <WiFi.h>

// Замените на свой идентификатор и пароль
const char* ssid = "help me";
const char* password = "2pidorazaebali";

// Номер порта для сервера
WiFiServer server(80);

// HTTP-запрос
String header;

// текущее состояние кнопки
String output26State = "off";
String output27State = "off";

// Номера выводов
const int output26 = 26;
const int output27 = 27;

void setup() {
  Serial.begin(115200);
  // Настраиваем выводы платы
  pinMode(output26, OUTPUT);
  pinMode(output27, OUTPUT);
  // Переводим выводы в LOW
  digitalWrite(output26, LOW);
  digitalWrite(output27, LOW);

  // Подключаемся к Wi-Fi
  Serial.print("Connecting to ");
  Serial.println(ssid);
  WiFi.begin(ssid, password);
  while (WiFi.status() != WL_CONNECTED) {
    delay(500);
    Serial.print(".");
  }
  // Выводим локальный IP-адрес и запускаем сервер
  Serial.println("");
  Serial.println("WiFi connected.");
  Serial.println("IP address: ");
  Serial.println(WiFi.localIP());
  server.begin();
}

void loop() {
  WiFiClient client = server.available(); // прослушка входящих клиентов
  if (client) { // Если подключается новый клиент,
    Serial.println("New Client."); // выводим сообщение
    String currentLine = "";
    while (client.connected()) { // цикл, пока есть соединение клиента
      if (client.available()) { // если от клиента поступают данные,
        char c = client.read(); // читаем байт, затем
        Serial.write(c); // выводим на экран
        header += c;
        if (c == '\n') { // если байт является переводом строки
          // если пустая строка, мы получили два символа перевода строки
          // значит это конец HTTP-запроса, формируем ответ сервера:
          if (currentLine.length() == 0) {
            // HTTP заголовки начинаются с кода ответа (напр., HTTP / 1.1 200 OK)
            // и content-type, затем пустая строка:
            client.println("HTTP/1.1 200 OK");
            client.println("Content-type:text/html");
            client.println("Connection: close");
            client.println();

            // Включаем или выключаем светодиоды
            if (header.indexOf("GET /26/on") >= 0) {
              Serial.println("GPIO 26 on");
              output26State = "on"; //добавить проверку на то, что замок еще не открылся в цикле
              digitalWrite(output26, HIGH);
            } else if (header.indexOf("GET /26/off") >= 0) {
              Serial.println("GPIO 26 off");
              output26State = "off"; //дверь закрыта
              digitalWrite(output26, LOW);
            } else if (header.indexOf("GET /27/on") >= 0) {
              Serial.println("GPIO 27 on");
              output27State = "on"; //добавить проверку на то, что замок еще не открылся в цикле
              digitalWrite(output27, HIGH);
            } else if (header.indexOf("GET /27/off") >= 0) {
              Serial.println("GPIO 27 off");
              output27State = "off"; //дверь закрыта
              digitalWrite(output27, LOW);
            }
            // Формируем веб-страницу на сервере
            client.println("<!DOCTYPE html><html>");
            client.println("<head><meta name=\"viewport\" content=\"width=device-width, initial-scale=1\">");
            client.println("<link rel=\"icon\" href=\"data:,\">");
            // CSS для кнопок
            // можете менять под свои нужды
            client.println("<style>html { font-family: Helvetica; display: inline-block; margin: 0px auto; text-align: center;}");
            client.println(".button { background-color: #4CAF50; border:  none; color: white; padding: 16px 40px;");
            client.println("text-decoration: none; font-size: 30px; margin: 2px; cursor: pointer;}");
            client.println(".button2 {background-color:#555555;}</style></head>");
            client.println("<body><h1>ESP32 Web Server</h1>");
            // Выводим текущее состояние кнопок
            client.println("<p>GPIO 26 - State " + output26State + "</p>");
            // Если output26State сейчас off, то выводим надпись ON
            if (output26State == "off") {
              client.println("<p><a href=\"/26/on\"><button class=\"button\">ON</button></a></p>");
            } else {
              client.println("<p><a href=\"/26/off\"><button class=\"button button2\">OFF</button></a></p>");
            }
            // Аналогично для второй кнопки
            client.println("<p>GPIO 27 - State " + output27State + "</p>");
            if (output27State == "off") {
              client.println("<p><a href=\"/27/on\"><button class=\"button\">ON</button></a></p>");
            } else {
              client.println("<p><a href=\"/27/off\"><button class=\"button button2\">OFF</button></a></p>");
            }
            client.println("</body></html>");
            // HTTP-ответ завершается пустой строкой
            client.println();
            break;
          } else { // если получили новую строку, очищаем currentLine
            currentLine = "";
          }
        } else if (c != '\r') { // Если получили что-то ещё кроме возврата строки,
          currentLine += c; // добавляем в конец currentLine
        }
      }
    }
    // Очистим переменную
    header = "";
    // Закрываем соединение
    client.stop();
    Serial.println("Client disconnected.");
    Serial.println("");
  }
  // else {
  //   if (output26State == "on") { //добавить проверку на то, что дверь закрылась
  //     Serial.println("Door unlocked");
  //     client.println("HTTP/1.1 200 OK");
  //     client.println("Content-type:text/html");
  //     client.println("Connection: close");
  //     client.println();

  //     // Формируем веб-страницу на сервере
  //     client.println("<!DOCTYPE html><html>");
  //     client.println("<head><meta name=\"viewport\" content=\"width=device-width, initial-scale=1\">");
  //     client.println("<link rel=\"icon\" href=\"data:,\">");
  //     // CSS для кнопок
  //     // можете менять под свои нужды
  //     client.println("<style>html { font-family: Helvetica; display: inline-block; margin: 0px auto; text-align: center;}");
  //     client.println(".button { background-color: #4CAF50; border:  none; color: white; padding: 16px 40px;");
  //     client.println("text-decoration: none; font-size: 30px; margin: 2px; cursor: pointer;}");
  //     client.println(".button2 {background-color:#555555;}</style></head>");
  //     client.println("<body><h1>ESP32 Web Server</h1>");
  //     // Выводим текущее состояние кнопок
  //     client.println("<p>GPIO 26 - State " + output26State + "</p>");
  //     // Если output26State сейчас off, то выводим надпись ON
  //     client.println("<p><a href=\"/26/off\"><button class=\"button button2\">OFF</button></a></p>");
  //     output26State = "off";
      
  //     // Аналогично для второй кнопки
  //     client.println("<p>GPIO 27 - State " + output27State + "</p>");
  //     if (output27State == "off") {
  //       client.println("<p><a href=\"/27/on\"><button class=\"button\">ON</button></a></p>");
  //     } else {
  //       client.println("<p><a href=\"/27/off\"><button class=\"button button2\">OFF</button></a></p>");
  //     }
  //     client.println("</body></html>");
  //     // HTTP-ответ завершается пустой строкой
  //     client.println();
  //   }
  //   else if (output27State == "on") { //добавить проверку на то, что дверь закрылась
  //     Serial.println("Door unlocked");
  //     client.println("HTTP/1.1 200 OK");
  //     client.println("Content-type:text/html");
  //     client.println("Connection: close");
  //     client.println();

  //     // Формируем веб-страницу на сервере
  //     client.println("<!DOCTYPE html><html>");
  //     client.println("<head><meta name=\"viewport\" content=\"width=device-width, initial-scale=1\">");
  //     client.println("<link rel=\"icon\" href=\"data:,\">");
  //     // CSS для кнопок
  //     // можете менять под свои нужды
  //     client.println("<style>html { font-family: Helvetica; display: inline-block; margin: 0px auto; text-align: center;}");
  //     client.println(".button { background-color: #4CAF50; border:  none; color: white; padding: 16px 40px;");
  //     client.println("text-decoration: none; font-size: 30px; margin: 2px; cursor: pointer;}");
  //     client.println(".button2 {background-color:#555555;}</style></head>");
  //     client.println("<body><h1>ESP32 Web Server</h1>");
  //     // Выводим текущее состояние кнопок
  //     client.println("<p>GPIO 26 - State " + output26State + "</p>");
  //     // Если output26State сейчас off, то выводим надпись ON
  //     if (output26State == "off") {
  //       client.println("<p><a href=\"/26/on\"><button class=\"button\">ON</button></a></p>");
  //     } else {
  //       client.println("<p><a href=\"/26/off\"><button class=\"button button2\">OFF</button></a></p>");
  //     }
  //     // Аналогично для второй кнопки
  //     client.println("<p>GPIO 27 - State " + output27State + "</p>");
  //     client.println("<p><a href=\"/27/off\"><button class=\"button button2\">OFF</button></a></p>");
  //     output27State = "off";
  //     client.println("</body></html>");
  //     // HTTP-ответ завершается пустой строкой
  //     client.println();
  //   }
  // }
}
