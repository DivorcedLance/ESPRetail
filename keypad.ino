#include <Keypad.h>
#include <Wire.h>               /*~ Librería I2C ~*/
#include <LiquidCrystal_I2C.h>  /*~ Librería LCD ~*/

void noop() {
  Serial.println("Noop");
}

// ================ Hardware ================

void setupLcd() {
  lcd.init();
  lcd.backlight();
  delay ( 1000 );
  lcd.noBacklight ( );
  delay ( 1000 );
  lcd.backlight();
  lcd.clear();
}

const uint8_t ROWS = 4;
const uint8_t COLS = 4;
char keys[ROWS][COLS] = {
  { '1', '2', '3', 'A' },
  { '4', '5', '6', 'B' },
  { '7', '8', '9', 'C' },
  { '*', '0', '#', 'D' }
};

uint8_t colPins[COLS] = { 12, 13, 32, 33 }; // Pins connected to C1, C2, C3, C4
uint8_t rowPins[ROWS] = { 25, 26, 27, 14 }; // Pins connected to R1, R2, R3, R4

Keypad keypad = Keypad(makeKeymap(keys), rowPins, colPins, ROWS, COLS);

LiquidCrystal_I2C lcd ( 0x27, 20, 4 );  /*~ Instancia de la clase para el manejo de la pantalla ( Dirección I2C, cantidad de columnas, cantidad de filas ) ~*/

// ================ Display Basics ================

// Cursor
int currentX = 0;
int currentY = 0;

void moveCursor(int x, int y) {
    lcd.setCursor(x, y);
    currentX = x;
    currentY = y;
}

void clearChar(int x, int y) {
    moveCursor(x, y);
    lcd.print(" ");
}

void writeChar(char c, int x, int y) {
    moveCursor(x, y);
    lcd.print(c);
}

void writeRow (int row, String text) {
    lcd.setCursor(0, row);
    if (text.length() > 20) {
        text = text.substring(0, 20);
    }
    lcd.print(text);
}

void clearRow(int row) {
    writeRow(row, "                    ");
}

// ================ Display Utilities ================

void setFooter (String footerText) {
    writeRow(3, footerText);
}

void write3Options (String* displayedOptions) {
    for (int i = 0; i < 3; i++) {
        writeRow(i, displayedOptions[i]);
    }
}

void display3Options (String* options, int nOptions, int index) {
  if (index + 2 < nOptions) {
    String displayedOptions[] = {options[index], options[index + 1], options[index + 2]};
    write3Options(displayedOptions);
  }
  // !: Handle index + 2 >= nOptions
}

// Globals
int typeDisplay;

int displayIndex;
String inputFooter;
int selectorY;
int pag;
String inputText;

// ==============

String* itemsList;
int nItems;

String* descuentosList;
int nDescuentos;

int* productsList;
int nproductos;
bool isVista;
int productsIndex;
int productsSelectorY;

// ================ Display 0 ================

// Variables Display 0
String* options;
int nOptions;
int selectedOption;
int optionSelectorY;

// Estados Display 0
int currentStateD0;
int nStatesD0;
int nextFCodeD0;

// Menu Principal
String menu_principal_options[] = {"Nueva Venta", "Shopper", "Tarjeta X", "Consulta EAN", "Tipo de Cambio", "Menu Supervisor"};
// Menu Caja
String menu_caja_options[] = {"Anular Item", "Consulta EAN", "Descuentos", "Tipo de Cambio", "Consulta Tarjeta X", "Suspender", "Retomar", "Redimir Cupón", "Items Faltantes Shop", "Anular Transacción"};


// ================ Display 1 ================

// Variables Display 1
String label;

// Estados Display 1
String* d1_labels;
int currentStateD1;
int nStatesD1;
int nextFCodeD1;

// Login
String login_labels[] = {"Inserte Operador", "Inserte Clave Operador", "Inserte Autorizador", "Inserte Clave Autorizador"};

// ================ CallBack Implementation ================

void callFunctionCode (int code) {
    switch (code) {
        case 0:
            login();
            break;
        case 1:
            menuPrincipal();
            break;
        default:
            break;
    }
}

// ================ Handle Displays ================

void updateInputText (String newText) {
    clearRow(3);
    writeRow(3, newText);
}

void writeInInput (char c) {
  // TODO: Handle better length > 20
  if (inputText.length() > 20) {
    return;
  }
  inputText = inputText.substring(0, inputText.length() - 1);
  inputText += c;
  inputText += '_';
  updateInputText(inputText);
}

void deleteInInput () {
  inputText = inputText.substring(0, inputText.length() - 2);
  inputText += '_';
  updateInputText(inputText);
}

// ================ Display 0 ================

void initDisplay0 (String* options_, int nOptions_) {
    typeDisplay = 0;
    
    options = options_;
    nOptions = nOptions_;
    optionSelectorY = 0;
    selectedOption = 0;

    inputText = "_";
    updateDisplay0();
}

void updateDisplay0 () {
    display3Options(options, nOptions, optionSelectorY);
    updateInputText(inputText);
    updateSelectedOption(selectedOption);
}

void updateSelectedOption (int index) {

}
// Implementar manejo de selected option con asterisco

void writeAsterisc(int row) {
    writeChar('*', 19, row);
}

// ================ Display 1 ================

void initDisplay1 (String labelText) {
    typeDisplay = 1;

    label = labelText;

    inputText = "_";
    updateDisplay1();
}

void updateDisplay1 () {
    updateLabelText(label);
    updateInputText(inputText);
}

void updateLabelText (String newText) {
    clearRow(1);
    // TODO: Handle better length > 20
    if (newText.length() > 20) {
        newText = newText.substring(0, 20);
    }
    writeRow(1, newText);
}

void nextDisplay1(int jump) {  
  if (currentStateD1+jump <= nStatesD1) {
    initDisplay1(d1_labels[currentStateD1 + jump]);
  } else {
    callFunctionCode(nextFCodeD1);
  }
}

void next(int jump = 1) {
  // TODO: Handle transition

  switch (typeDisplay)
  {
  case 1:
    nextDisplay1(jump);
    break;
  
  default:
    break;
  }


}

// ================ Display 0 ================

void menuPrincipal() {
  initDisplay0("Menu Principal", menu_principal_options, 10);
}

// ================ Display 1 ================

void login() {
  d1_labels = login_labels;
  nStatesD1 = 4;
  nextFCodeD1 = 1;
  currentStateD1 = 0;
  initDisplay1(d1_labels[currentStateD1]);
}

void onKeyPress ( char key ) {
    switch ( typeDisplay ) {
        case 1:
          if (key == 'A') {
            if ((inputText.length() == 1) && (currentStateD1 != 0)) {
              next(-1);
            } else {
              deleteInInput();
            }
          } else if ((key == 'B')||(key == 'C')) {
            noop();
          } else if (key == 'D') {
            next(1);
          } else {
            writeInInput(key);
          }
          break;
        default:
          break;
    }
}

void setup ( void ) {
  setupLcd();
  Serial.begin(115200);
  login();
} 

void loop ( void ) {
    char key = keypad.getKey();
    if (key != NO_KEY) {
        onKeyPress(key);
    }
}