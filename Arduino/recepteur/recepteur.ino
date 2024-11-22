// Constantes paramètres du montage

int phot = 0;    // pin GPIO de la photodiode
int led = LED_BUILTIN;    // témoin de transfert d'information: si la led est allumée alors pas de transfert en cours

int periode_echantillon = 500; // temps d'éclairement ou d'extinction de la led. Doit etre égal à la variable periode_echantillon coté émetteur
int temps_initial = 500;       // temps d'attente après le premier allumage indiquant le début du signal
int seuil_eclairage = -200;     // seuil au delà duquel le signal capté est considéré à 1

// Variables globales

int acqu;               // variable stockant acquisition analogique de la photodiode
char resultat;          // variable de type char pour stocker le caractère reçu

void setup()
{
    Serial.begin(9600);
    pinMode(phot, INPUT);
    pinMode(led, OUTPUT);
}    

/** 
 * L'implémentation suivante utilise un seul passage dans loop() 
 * pour les l'octet reçu en entier, avec des temps de delay conséquents.
 * Ces delay coupent tout fonctionnement de la carte pendant un certain
 * temps, ce qui peut s'avérer problématique.
*/
void loop() 
{
    digitalWrite(led, HIGH);
    acqu = -analogRead (phot);

    if (acqu > seuil_eclairage) {
        digitalWrite(led, LOW);

        Serial.println("\n-----\nDébut de la réception\n-----\n");
        delay(temps_initial);


        for (int i = 0; i < 8; i++) {
            acqu = -analogRead(phot);

            resultat = resultat << 1; // Cette opération décale le nombre binaire qui représente résultat de 1 vers la gauche ("Bit Shift")
            int ajout = acqu > seuil_eclairage ? 1 : 0;
            Serial.println(ajout);
            resultat += ajout;        // Ajoute 1 si le seuil est dépassé, 0 sinon ("Ternary Operator ")

            delay(periode_echantillon);
        }

        Serial.println("Réception effectuée.\n");

        Serial.println((int)resultat);

        if (resultat < 'a' || resultat > 'z') {
            Serial.println("Erreur: Mauvaise émission ou problème de lecture; la lettre reconnue n'est pas une lettre minuscule\n");
        } else {
            Serial.print("Lettre reçue : ");
            Serial.println(resultat);
        }
    }

    delay(10);
}