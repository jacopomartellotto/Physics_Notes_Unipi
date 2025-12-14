/* 
Questo sketch serve per acquisire 8192 misure sulla porta A0 di Arduino Due e trasferirle al PC 
In abbinamento allo script arducal.py, permette di creare un file di 8192 coppie di dati
tempo in microsecondi e d.d.p. in digit
*/

// Blocco definizioni
const unsigned int analogPin=0; // Definisce la porta A0 per la lettura
const int digitalPin_uno=7; // Definisce la porta 7 usata come output ref
int i; // Definisce la variabile intera i (contatore dei cicli di lettura e scrittura)
int delays = 100; // Definisce la variabile intera delays (ritardo in microsecondi fra una digitalizzazione e la successiva, qui regolata a 100 us)
int V[8192]; // Definisce l'array intero V che contiene le letture
long t[8192]; // Definisce l'array t che contiene il tempo della lettura, in microsecondi
unsigned long StartTime; // Definisce il valore StartTime
int start=0; // Definisce il valore start (usato come flag)
int dummy; // Definisce la variabile usata per leggere la porta seriale

// Istruzioni di inizializzazione
void setup()
  {
   Serial.begin(119200); // Inizializza la porta seriale a 119200 baud
   Serial.flush(); // Pulisce il buffer della porta seriale 
   digitalWrite(digitalPin_uno,HIGH); // Pone digitalPin_uno a livello alto
   analogReadResolution(12);// Istruisce il digitalizzatore di usare la risoluzione, o dinamica, a 12 bit (livelli di uscita tra 0 e 4095 digit)
  }

// Istruzioni del programma
void loop()
  {
    if (Serial.available() >0) // Controlla se il buffer seriale ha qualcosa
      {
      dummy=Serial.read();
	start=1; // Nel caso ci sia qualcosa, pone il flag start a uno
      }
 
  if(!start) return // Se il flag e' start=0 non esegue le operazioni qui di seguito
                    // altrimenti le fa partire 
    delay(2000); // Aspetta 2000 ms per evitare casini 

     for(i=0;i<2;i++) // Fa un ciclo di due letture a vuoto per "scaricare" l'analogPin ed evitare artefatti
       {
        V[i]=analogRead(analogPin);
       }
    StartTime=micros(); // Misura il tempo iniziale con l'orologio interno
    for(i=0;i<8192;i++) // Loop di misura 
      {
          t[i]=micros()-StartTime; // Legge il timestamp e lo mette in array t
          V[i]=analogRead(analogPin); // Legge analogPin e lo mette in array V
          delayMicroseconds(delays); // Aspetta tot us
      }
  
    for(i=0;i<8192;i++) // Loop per la scrittura su porta seriale
      {
        Serial.print(t[i]); // Scrive t[i]
        Serial.print(" "); // Mette uno spazio
        Serial.println(V[i]); // Scrive V[i] e va a capo
      }
  
    start=0; // Annulla il flag, cioe' fa terminare il programma
    Serial.flush(); // Pulisce il buffer della porta seriale (si sa mai)
}
