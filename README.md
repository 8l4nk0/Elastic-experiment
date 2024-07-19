<h1>Elastic-experiment<br><br>

Questo piccolo progetto prevede di collegare il SIEM Elastic ad una macchina virtuale (VM) Kali Linux tramite Elastic Agent per registrarne gli eventi sottoforma di log e rappresentarli graficamente su una dashboard personalizzata dopo aver inserito la/e regola/e per filtrare i log che ci interessano.<br>

Requisiti:<br>
- Creazione account gratuito un mese di Elastic<br>
- VM Kali Linux<br><br>


Fase 1)<br>
Cliccare sul menù in alto a sinistra (le tre linee piccole) e scorri in basso fino ad Integrations.<br>
Cerca Elastic Defend e cliccalo.<br>
Clicca in alto a destra su Add Elastic Defend.<br>
Clicca in basso Install Elastic Agent (questo per collegare Elastic alla VM Kali Linux in modo tale da poter registrare gli eventi della VM sottoforma di Logs).<br><br>


Fase 2)<br>
Cliccando su Install Elastic Agent, seleziona Linux e incolliamo questo comando nel terminale della VM:<br>
--------------------------------------------------------------------------------------------------------<br>
curl -L -O https://artifacts.elastic.co/downloads/beats/elastic-agent/elastic-agent-8.14.3-linux-x86_64.tar.gz<br>
tar xzvf elastic-agent-8.14.3-linux-x86_64.tar.gz<br>
cd elastic-agent-8.14.3-linux-x86_64<br>
sudo ./elastic-agent install --url=https://5630fedb9fa4401c803f73336462c375.fleet.westus2.azure.elastic-cloud.com:443 --enrollment-<br>token=ZWVoN3dKQUI4YkVDZmJnekViYXo6RW83YUlqTjZUTy00N2l3VW9OckVYdw==<br>
--------------------------------------------------------------------------------------------------------<br>
In questo modo abbiamo collegato il SIEM Elastic alla nostra VM tramite l'agent "Elastic Agent".<br><br>


Fase 3)<br>
Grazie allo strumento di recognizione di rete, NMAP, possiamo effettuare delle scansioni della rete per generare gli alert nel nostro SIEM per verificare
se tutto sia ben collegato.<br>
Andiamo nel menù in alto a sinistra (le tre linee piccole) e clicchiamo su Logs per vedere se il SIEM ha captato i nostri tentativi di mappaggio con Nmap.<br>
Qui avremo la lista dei vari logs registrati dal SIEM. Filtrando per <process.args:"nmap"> vedremo tutti i nostri tentativi fatti. In particolare cliccandone<br>
uno e poi sui tre puntini vedremo i dettagli, compreso il comando inserito con quale permessi e da quale macchina.<br><br>


Fase 4)<br>
Infine andiamo nel menù in alto a sinistra (le tre linee piccole) su Analytics -> Dashboard -> Create Dashboard -> Create Visualization.<br>
Questo ci permetterà di rappresentare graficamente i log. Per una semplice visualizzazione cerchiamo "Area" oppure "Line".<br>
Io ho scelto Area e impostato Count sull'asse verticale e Timestamp sull'asse orizzontale.<br><br>


Fase 5)<br>
Infine andiamo nel menù in alto a sinistra (le tre linee piccole) su Security-> Alerts-> Manage Rules-> Create New Rule->Custom Query.<br>
Qui costruiamo la regola per il nostro SIEM per eventi particolari.<br>
Per esempio impostando la query come:<br><br>

process.args:"nmap"<br><br>

stiamo indicando che il SIEM deve creare un alert per gli scan con Nmap.<br>
Andando avanti, nella sezione About Rule le diamo un nome e ne descriviamo lo scopo.<br>
Impostiamo il livello di sicurezza ad High.<br>
Nella sezione Schedule, io ho impostato 3 minuti di frequenza e 1 minuto di lookback perchè voglio che controlli spesso se si verificano eventi di questo genere.<br>
Infine nella sezione Actions possiamo decidere come "reagisce" il SIEM, ossia  nel momento in cui individua dei tentativi di nmap_scan
allora gli possiamo indicare di inviare una mail, inviare un link su Slack... (per avvertire il team di Sicurezza è molto utile, soprattutto per
eventi particolarmente critici). <br>
E' possibile anche impostare più di un trigger(reazione) perciò si possono fare anche combinazioni di comunicazioni nel caso,
per esempio, fosse necessario avvertire il team di Sicurezza, il team di Rete, i dipendenti in ufficio, il caporeparto...
Qui io ho impostato come "reazione" inviare una mail al mio indirizzo ogni 10 minuti.<br><br>


Fase 6)<br>
Perfetto, adesso nella sezione Security -> Alerts potremo vedere gli alert che verranno generati nel caso in cui la regola che abbiamo creato dovesse attivarsi.<br>
Mentre nella sezione Analytics -> Dashboards potremo vedere il grafico.<br><br>



Extra)<br>

Per testare un pò di cose ho scritto un piccolo script in Python per generare traffico di rete così da avere uno spettro di eventi più variegato.<br>
Per lo script ho utilizzato anche Scapy, una libreria che serve per creare, manipolare e analizzare pacchetti di rete in parole povere.<br><br>

Poi ho scritto un piccolo script per tentare l'accesso non autorizzato con SSH su porta 22 utilizzando combinazioni di 5 username e 5 password casuali.<br>
Per questo script ho usato la libreria Paramiko, che implementa il protocollo SSHv2 provvedendo sia al client che al server.<br>
Siccome sulla mia VM non era aperta la porta 22 per il protocollo SSH ho dovuto prima installare il server OpenSSH da riga di comando:<br><br>

sudo apt-get install openssh-server<br><br>

Poi l'ho avviato con:<br><br>

sudo systemctl start ssh<br><br>

E infine ho abilitato il firewall (non era attivo) e ho modificato la regola che ci consente la connessione verso la porta 22:<br>
- sudo ufw enable<br>
- sudo ufw allow 22/tcp<br>
- sudo ufw reload<br><br><br>


Per vedere se SSH è attivo:<br>
- sudo systemctl status ssh<br><br>

Infine ho creato una nuova regola che filtrasse i log per tentativi che includevano i comandi ssh e sshpass.<br>

