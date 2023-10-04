/*
int abruzzo = 22;
int basilicata = 23;
int calabria = 24;
int campania = 25;
int emilia = 26;
int firuli = 27;
int lazio = 28;
int liguria = 29;
int lombardia = 30;
int marche = 31;
int molise = 32;
int piemonte = 33;
int puglia = 34;
int sardegna = 35;
int sicilia = 36;
int toscana = 37;
int trentino = 38;
int umbria = 39;
int aosta = 40;
int veneto = 41;
*/
int verde=12;
int rosso=13;
int regioni[20] = {52,51,50,49,48,47,46,45,44,43,42,41,40,39,38,37,36,35,34,33};
char res;
void setup() {
  for(int i=0;i<20;i++){
    pinMode(regioni[i], INPUT);
  }
  pinMode(rosso, OUTPUT);
  pinMode(verde, OUTPUT);
  Serial.begin(9600);
}
/*
pinMode(abruzzo,INPUT);
pinMode(basilicata,INPUT);
pinMode(calabria,INPUT);
pinMode(campania,INPUT);
pinMode(emilia,INPUT);
pinMode(firuli,INPUT);
pinMode(lazio,INPUT);
pinMode(liguria,INPUT);
pinMode(lombardia,INPUT);
pinMode(marche,INPUT);
pinMode(molise,INPUT);
pinMode(piemonte,INPUT);
pinMode(puglia,INPUT);
pinMode(sardegna,INPUT);
pinMode(sicilia,INPUT);
pinMode(toscana,INPUT);
pinMode(trentino,INPUT);
pinMode(umbria,INPUT);
pinMode(aosta,INPUT);
pinMode(veneto,INPUT);
*/
int var;
void loop() {
  for(int i=0;i<20;i++){
    var = digitalRead(regioni[i]);
    if(var==HIGH){
      // digitalWrite(verde, HIGH);

      Serial.write(regioni[i]);
      res = Serial.read();
      if(res == 'c'){
        digitalWrite(verde, HIGH);
        delay(1000);
        digitalWrite(verde, LOW);
      } else if (res == 'w') {
        digitalWrite(rosso, HIGH);
        delay(1000);
        digitalWrite(rosso, LOW);
      }
    }
      // digitalWrite(verde, LOW);
  }
}
