#include <WiFi.h>
#include "esp_wifi.h"

#define ssd "INTELBRAS"
#define senha "afa123123"
#define SERVER_PORT 5000

void sniffer(void* buf, wifi_promiscuous_pkt_type_t type);

struct send_data{
  String end_mac;
  int intensidade;  
};

const wifi_promiscuous_filter_t filt={ //Idk what this does
    .filter_mask=WIFI_PROMIS_FILTER_MASK_MGMT|WIFI_PROMIS_FILTER_MASK_DATA
};

typedef struct { // or this
  uint8_t mac[6];
} __attribute__((packed)) MacAddr;

typedef struct { // still dont know much about this
  int16_t fctl;
  int16_t duration;
  MacAddr da;
  MacAddr sa;
  MacAddr bssid;
  int16_t seqctl;
  unsigned char payload[];
} __attribute__((packed)) WifiMgmtHdr;


struct send_data dados;

char msg[15];

void setup(){


  wifi_init_config_t cfg = WIFI_INIT_CONFIG_DEFAULT();
  esp_wifi_init(&cfg);
  esp_wifi_set_storage(WIFI_STORAGE_RAM);
  esp_wifi_set_mode(WIFI_MODE_NULL);
  esp_wifi_start();
  esp_wifi_set_promiscuous(true);
  esp_wifi_set_promiscuous_filter(&filt);
  esp_wifi_set_promiscuous_rx_cb(&sniffer);
  esp_wifi_set_channel(11, WIFI_SECOND_CHAN_NONE);
  
  Serial.println("starting!");

  Serial.begin(115200);
  WiFi.begin(ssd, senha);
  
  while (WiFi.status() != WL_CONNECTED){ 
    Serial.print(".");   
    delay(500);
  }
  Serial.println(WiFi.localIP());
}
 
 
void loop(){

    esp_wifi_set_channel(11, WIFI_SECOND_CHAN_NONE);
    
    WiFiClient client;
    
    if (!client.connect("192.168.0.8", SERVER_PORT)){
        Serial.println("Servidor nao encontrado!");
        return;
    }

    dados.end_mac +="_DB="+String(dados.intensidade);
    char vet[dados.end_mac.length()+1];
    dados.end_mac.toCharArray(vet, dados.end_mac.length());
    Serial.println(msg);
    client.write(msg);
    client.flush();
    client.stop();
}
//Encerra o #ifndef do começo do arquivo


void sniffer(void* buf, wifi_promiscuous_pkt_type_t type) { //This is where packets end up after they get sniffed
  wifi_promiscuous_pkt_t *p = (wifi_promiscuous_pkt_t*)buf; // Dont know what these 3 lines do
  int len = p->rx_ctrl.sig_len;
  WifiMgmtHdr *wh = (WifiMgmtHdr*)p->payload;
  len -= sizeof(WifiMgmtHdr);
  if (len < 0){
    Serial.println("Receuved 0");
    return;
  }
  String packet;
  String mac;
  int fctl = ntohs(wh->fctl);
  for(int i=8;i<=8+6+1;i++){ // This reads the first couple of bytes of the packet. This is where you can read the whole packet replaceing the "8+6+1" with "p->rx_ctrl.sig_len"
     packet += String(p->payload[i],HEX);
  }
  
  for(int i=4;i<=15;i++){ // This removes the 'nibble' bits from the stat and end of the data we want. So we only get the mac address.
    mac += packet[i];
    msg[i-4] = packet[i];
  }
  mac.toUpperCase();


  int db = p->rx_ctrl.rssi;
      /*Serial.print("MAC --> ");
      Serial.print(mac);
      Serial.print("\nDB --> ");
      Serial.println(db);*/
  dados.end_mac = mac;
  dados.intensidade = db;
  msg[10]='_';
  for(int i=0;i<String(db).length();i++) msg[11+i]=String(db)[i];
}
