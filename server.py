from flask import Flask, request, jsonify, send_from_directory
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
import random

app = Flask(__name__, static_folder='.', static_url_path='')

# حماية السيرفر من الـ DDoS و Spam Requests
limiter = Limiter(
    get_remote_address,
    app=app,
    default_limits=["100 per minute"],
    storage_uri="memory://",
)

# =========================================================
# كتالوج اللابات (50+ أداة وثغرة) - جاهز للتعديل
# =========================================================
TOOLS_DB = {
    # --- Web Vulns (PortSwigger) ---
    "sql_injection": {"name": "SQL Injection", "links": {"easy": "https://portswigger.net/web-security/sql-injection/lab-retrieve-hidden-data", "medium": "https://portswigger.net/web-security/sql-injection/union-attacks/lab-retrieve-multiple-values-in-single-column", "hard": "https://portswigger.net/web-security/sql-injection/blind/lab-time-delays-info-retrieval"}},
    "xss": {"name": "Cross-Site Scripting (XSS)", "links": {"easy": "https://portswigger.net/web-security/cross-site-scripting/reflected/lab-html-context-nothing-encoded", "medium": "https://portswigger.net/web-security/cross-site-scripting/stored/lab-html-context-nothing-encoded", "hard": "https://portswigger.net/web-security/cross-site-scripting/dom-based/lab-document-write-sink"}},
    "csrf": {"name": "Cross-Site Request Forgery", "links": {"easy": "https://portswigger.net/web-security/csrf/lab-no-defenses", "medium": "https://portswigger.net/web-security/csrf/lab-token-validation-depends-on-request-method", "hard": "https://portswigger.net/web-security/csrf/lab-samesite-lax-bypass-via-method-override"}},
    "ssrf": {"name": "Server-Side Request Forgery", "links": {"easy": "https://portswigger.net/web-security/ssrf/lab-basic-ssrf-against-localhost", "medium": "https://portswigger.net/web-security/ssrf/lab-basic-ssrf-against-backend-system", "hard": "https://portswigger.net/web-security/ssrf/blind/lab-out-of-band-detection"}},
    "xxe": {"name": "XML External Entity (XXE)", "links": {"easy": "https://portswigger.net/web-security/xxe/lab-exploiting-xxe-to-retrieve-files", "medium": "https://portswigger.net/web-security/xxe/blind/lab-xxe-with-out-of-band-interaction", "hard": "https://portswigger.net/web-security/xxe/blind/lab-xxe-with-out-of-band-interaction-using-parameter-entities"}},
    "access_control": {"name": "Broken Access Control", "links": {"easy": "https://portswigger.net/web-security/access-control/lab-unprotected-admin-functionality", "medium": "https://portswigger.net/web-security/access-control/lab-user-role-controlled-by-request-parameter", "hard": "https://portswigger.net/web-security/access-control/lab-referer-based-access-control"}},
    "auth": {"name": "Authentication Vulnerabilities", "links": {"easy": "https://portswigger.net/web-security/authentication/password-based/lab-username-enumeration-via-different-responses", "medium": "https://portswigger.net/web-security/authentication/multi-factor/lab-2fa-broken-logic", "hard": "https://portswigger.net/web-security/authentication/password-based/lab-broken-brute-force-protection-multiple-credentials-per-request"}},
    "business_logic": {"name": "Business Logic Flaws", "links": {"easy": "https://portswigger.net/web-security/logic-flaws/examples/lab-logic-flaws-excessive-trust-in-client-side-controls", "medium": "https://portswigger.net/web-security/logic-flaws/examples/lab-logic-flaws-high-level", "hard": "https://portswigger.net/web-security/logic-flaws/examples/lab-logic-flaws-low-level"}},
    "command_injection": {"name": "OS Command Injection", "links": {"easy": "https://portswigger.net/web-security/os-command-injection/lab-simple", "medium": "https://portswigger.net/web-security/os-command-injection/lab-blind-time-delays", "hard": "https://portswigger.net/web-security/os-command-injection/lab-blind-out-of-band-data-exfiltration"}},
    "ssti": {"name": "Server-Side Template Injection", "links": {"easy": "https://portswigger.net/web-security/server-side-template-injection/exploiting/lab-server-side-template-injection-basic", "medium": "https://portswigger.net/web-security/server-side-template-injection/exploiting/lab-server-side-template-injection-in-an-unknown-language", "hard": "https://portswigger.net/web-security/server-side-template-injection/exploiting/lab-server-side-template-injection-with-a-custom-exploit"}},
    "deserialization": {"name": "Insecure Deserialization", "links": {"easy": "https://portswigger.net/web-security/deserialization/exploiting/lab-deserialization-modifying-serialized-objects", "medium": "https://portswigger.net/web-security/deserialization/exploiting/lab-deserialization-modifying-serialized-data-types", "hard": "https://portswigger.net/web-security/deserialization/exploiting/lab-deserialization-exploiting-java-deserialization-with-apache-commons-collections"}},
    "cors": {"name": "CORS Misconfiguration", "links": {"easy": "https://portswigger.net/web-security/cors/lab-basic-origin-reflection-attack", "medium": "https://portswigger.net/web-security/cors/lab-whitelisted-null-origin", "hard": "https://portswigger.net/web-security/cors/lab-breaking-tls-with-cors"}},
    "jwt": {"name": "JWT Attacks", "links": {"easy": "https://portswigger.net/web-security/jwt/lab-jwt-authentication-bypass-via-unverified-signature", "medium": "https://portswigger.net/web-security/jwt/lab-jwt-authentication-bypass-via-flawed-signature-verification", "hard": "https://portswigger.net/web-security/jwt/lab-jwt-authentication-bypass-via-jwk-header-injection"}},
    "websockets": {"name": "WebSockets Security", "links": {"easy": "https://portswigger.net/web-security/websockets/lab-manipulating-websocket-messages-to-exploit-vulnerabilities", "medium": "https://portswigger.net/web-security/websockets/lab-manipulating-the-handshake-to-exploit-vulnerabilities", "hard": "https://portswigger.net/web-security/websockets/lab-cross-site-websocket-hijacking"}},
    "info_disclosure": {"name": "Information Disclosure", "links": {"easy": "https://portswigger.net/web-security/information-disclosure/exploiting/lab-infoleak-in-error-messages", "medium": "https://portswigger.net/web-security/information-disclosure/exploiting/lab-infoleak-on-debug-page", "hard": "https://portswigger.net/web-security/information-disclosure/exploiting/lab-infoleak-via-backup-files"}},
    "path_traversal": {"name": "Path Traversal", "links": {"easy": "https://portswigger.net/web-security/file-path-traversal/lab-simple", "medium": "https://portswigger.net/web-security/file-path-traversal/lab-absolute-path-bypass", "hard": "https://portswigger.net/web-security/file-path-traversal/lab-superfluous-url-decode"}},
    "host_header": {"name": "HTTP Host Header Attacks", "links": {"easy": "https://portswigger.net/web-security/host-header/exploiting/lab-host-header-basic-password-reset-poisoning", "medium": "https://portswigger.net/web-security/host-header/exploiting/lab-host-header-host-header-authentication-bypass", "hard": "https://portswigger.net/web-security/host-header/exploiting/lab-host-header-routing-based-ssrf"}},
    "oauth": {"name": "OAuth Authentication", "links": {"easy": "https://portswigger.net/web-security/oauth/lab-oauth-authentication-bypass-via-oauth-implicit-flow", "medium": "https://portswigger.net/web-security/oauth/lab-oauth-forced-oauth-profile-linking", "hard": "https://portswigger.net/web-security/oauth/lab-oauth-account-hijacking-via-redirect-uri"}},
    "web_cache": {"name": "Web Cache Poisoning", "links": {"easy": "https://portswigger.net/web-security/web-cache-poisoning/exploiting-design-flaws/lab-web-cache-poisoning-with-an-unkeyed-header", "medium": "https://portswigger.net/web-security/web-cache-poisoning/exploiting-design-flaws/lab-web-cache-poisoning-with-an-unkeyed-query-parameter", "hard": "https://portswigger.net/web-security/web-cache-poisoning/exploiting-implementation-flaws/lab-web-cache-poisoning-targeted-using-unknown-header"}},
    "smuggling": {"name": "HTTP Request Smuggling", "links": {"easy": "https://portswigger.net/web-security/request-smuggling/lab-basic-cl-te", "medium": "https://portswigger.net/web-security/request-smuggling/lab-basic-te-cl", "hard": "https://portswigger.net/web-security/request-smuggling/exploiting/lab-bypassing-client-side-desync-defenses"}},
    "race_conditions": {"name": "Race Conditions", "links": {"easy": "https://portswigger.net/web-security/race-conditions/lab-race-conditions-limit-overrun", "medium": "https://portswigger.net/web-security/race-conditions/lab-race-conditions-bypassing-rate-limits", "hard": "https://portswigger.net/web-security/race-conditions/lab-race-conditions-exploiting-time-of-check-to-time-of-use"}},
    "prototype_pollution": {"name": "Prototype Pollution", "links": {"easy": "https://portswigger.net/web-security/prototype-pollution/client-side/lab-prototype-pollution-client-side-basic", "medium": "https://portswigger.net/web-security/prototype-pollution/client-side/lab-prototype-pollution-client-side-bypassing-filters", "hard": "https://portswigger.net/web-security/prototype-pollution/server-side/lab-prototype-pollution-server-side-basic"}},
    "graphql": {"name": "GraphQL API Vulnerabilities", "links": {"easy": "https://portswigger.net/web-security/graphql/lab-graphql-finding-exposed-graphql-endpoint", "medium": "https://portswigger.net/web-security/graphql/lab-graphql-accidental-field-exposure", "hard": "https://portswigger.net/web-security/graphql/lab-graphql-bypassing-rate-limits-using-aliases"}},
    "api_testing": {"name": "API Testing", "links": {"easy": "https://portswigger.net/web-security/api-testing/lab-exploiting-api-endpoint-to-buy-unintended-item", "medium": "https://portswigger.net/web-security/api-testing/lab-exploiting-server-side-parameter-pollution-in-api", "hard": "https://portswigger.net/web-security/api-testing/lab-exploiting-mass-assignment-in-api"}},
    "clickjacking": {"name": "Clickjacking", "links": {"easy": "https://portswigger.net/web-security/clickjacking/lab-basic-csrf-protected", "medium": "https://portswigger.net/web-security/clickjacking/lab-prefilled-form-input", "hard": "https://portswigger.net/web-security/clickjacking/lab-frame-busting-bypass"}},
    "dom_xss": {"name": "DOM-based Vulnerabilities", "links": {"easy": "https://portswigger.net/web-security/dom-based/controlling-the-dom/lab-dom-xss-using-web-messages", "medium": "https://portswigger.net/web-security/dom-based/controlling-the-dom/lab-dom-xss-using-document-write", "hard": "https://portswigger.net/web-security/dom-based/controlling-the-dom/lab-dom-clobbering-to-exploit-dom-xss"}},
    "file_upload": {"name": "File Upload Vulnerabilities", "links": {"easy": "https://portswigger.net/web-security/file-upload/lab-file-upload-remote-code-execution-via-web-shell-upload", "medium": "https://portswigger.net/web-security/file-upload/lab-file-upload-web-shell-upload-via-content-type-restriction-bypass", "hard": "https://portswigger.net/web-security/file-upload/lab-file-upload-web-shell-upload-via-path-traversal"}},
    
    # --- Network & System (TryHackMe / HTB) ---
    "nmap": {"name": "Nmap Scanning", "links": {"easy": "https://tryhackme.com/room/furthernmap", "medium": "https://tryhackme.com/room/nmap", "hard": "https://app.hackthebox.com/starting-point"}},
    "hydra": {"name": "Hydra Brute Force", "links": {"easy": "https://tryhackme.com/room/hydra", "medium": "https://tryhackme.com/room/bruteforce", "hard": "https://tryhackme.com/room/passwordattacks"}},
    "metasploit": {"name": "Metasploit Framework", "links": {"easy": "https://tryhackme.com/room/metasploitintro", "medium": "https://tryhackme.com/room/metasploit", "hard": "https://tryhackme.com/room/metasploitexploitation"}},
    "linux_privesc": {"name": "Linux PrivEsc", "links": {"easy": "https://tryhackme.com/room/linuxprivesc", "medium": "https://tryhackme.com/room/linuxprivesc", "hard": "https://tryhackme.com/room/linuxprivesc"}},
    "windows_privesc": {"name": "Windows PrivEsc", "links": {"easy": "https://tryhackme.com/room/windowsprivesc", "medium": "https://tryhackme.com/room/windows10privesc", "hard": "https://tryhackme.com/room/windowsprivesc"}},
    "wireshark": {"name": "Wireshark Traffic Analysis", "links": {"easy": "https://tryhackme.com/room/wireshark101", "medium": "https://tryhackme.com/room/wireshark", "hard": "https://tryhackme.com/room/wiresharkpackets"}},
    "gobuster": {"name": "Gobuster Directory Busting", "links": {"easy": "https://tryhackme.com/room/gobusterthebasics", "medium": "https://tryhackme.com/room/gobusterthebasics", "hard": "https://tryhackme.com/room/gobusterthebasics"}},
    "nikto": {"name": "Nikto Web Scanner", "links": {"easy": "https://tryhackme.com/room/nikto", "medium": "https://tryhackme.com/room/nikto", "hard": "https://tryhackme.com/room/nikto"}},
    "john": {"name": "John The Ripper", "links": {"easy": "https://tryhackme.com/room/johntheripperbasics", "medium": "https://tryhackme.com/room/johntheripperbasics", "hard": "https://tryhackme.com/room/johntheripperbasics"}},
    "hashcat": {"name": "Hashcat Cracking", "links": {"easy": "https://tryhackme.com/room/hashcat", "medium": "https://tryhackme.com/room/hashcat", "hard": "https://tryhackme.com/room/hashcat"}},
    "aircrack": {"name": "Aircrack-ng WiFi", "links": {"easy": "https://tryhackme.com/room/aircrackng", "medium": "https://tryhackme.com/room/aircrackng", "hard": "https://tryhackme.com/room/aircrackng"}},
    "bloodhound": {"name": "BloodHound AD", "links": {"easy": "https://tryhackme.com/room/bloodhound", "medium": "https://tryhackme.com/room/bloodhound", "hard": "https://tryhackme.com/room/bloodhound"}},
    "impacket": {"name": "Impacket Tools", "links": {"easy": "https://tryhackme.com/room/impacket", "medium": "https://tryhackme.com/room/impacket", "hard": "https://tryhackme.com/room/impacket"}},
    "chisel": {"name": "Chisel Pivoting", "links": {"easy": "https://tryhackme.com/room/chisel", "medium": "https://tryhackme.com/room/chisel", "hard": "https://tryhackme.com/room/chisel"}},
    "linpeas": {"name": "LinPEAS", "links": {"easy": "https://tryhackme.com/room/linpeas", "medium": "https://tryhackme.com/room/linpeas", "hard": "https://tryhackme.com/room/linpeas"}},
    "winpeas": {"name": "WinPEAS", "links": {"easy": "https://tryhackme.com/room/winpeas", "medium": "https://tryhackme.com/room/winpeas", "hard": "https://tryhackme.com/room/winpeas"}},
    
    # --- Local Deployed Labs (لو رفعتهم على Render غيرهم بالروابط بتاعتك) ---
    "dvwa": {"name": "DVWA", "links": {"easy": "https://vulnerables-web-dvwa.onrender.com", "medium": "https://vulnerables-web-dvwa.onrender.com", "hard": "https://vulnerables-web-dvwa.onrender.com"}},
    "juice_shop": {"name": "OWASP Juice Shop", "links": {"easy": "https://bkimminich-juice-shop.onrender.com", "medium": "https://bkimminich-juice-shop.onrender.com", "hard": "https://bkimminich-juice-shop.onrender.com"}},
    "bwapp": {"name": "bWAPP", "links": {"easy": "https://YOUR-BWAPP.onrender.com", "medium": "https://YOUR-BWAPP.onrender.com", "hard": "https://YOUR-BWAPP.onrender.com"}},
    "webgoat": {"name": "OWASP WebGoat", "links": {"easy": "https://YOUR-WEBGOAT.onrender.com", "medium": "https://YOUR-WEBGOAT.onrender.com", "hard": "https://YOUR-WEBGOAT.onrender.com"}},
    "mutillidae": {"name": "OWASP Mutillidae", "links": {"easy": "https://YOUR-MUTILLIDAE.onrender.com", "medium": "https://YOUR-MUTILLIDAE.onrender.com", "hard": "https://YOUR-MUTILLIDAE.onrender.com"}},
    "vampi": {"name": "VAmPI (API)", "links": {"easy": "https://YOUR-VAMPI.onrender.com", "medium": "https://YOUR-VAMPI.onrender.com", "hard": "https://YOUR-VAMPI.onrender.com"}},
    "sqli_lab": {"name": "SQLi Labs", "links": {"easy": "https://YOUR-SQLI.onrender.com", "medium": "https://YOUR-SQLI.onrender.com", "hard": "https://YOUR-SQLI.onrender.com"}},
    "xss_lab": {"name": "XSS Labs", "links": {"easy": "https://YOUR-XSS.onrender.com", "medium": "https://YOUR-XSS.onrender.com", "hard": "https://YOUR-XSS.onrender.com"}},
    "lfi_lab": {"name": "LFI / RFI Labs", "links": {"easy": "https://YOUR-LFI.onrender.com", "medium": "https://YOUR-LFI.onrender.com", "hard": "https://YOUR-LFI.onrender.com"}},
    "rce_lab": {"name": "RCE Labs", "links": {"easy": "https://YOUR-RCE.onrender.com", "medium": "https://YOUR-RCE.onrender.com", "hard": "https://YOUR-RCE.onrender.com"}},
    "ssrf_lab": {"name": "SSRF Labs", "links": {"easy": "https://YOUR-SSRF.onrender.com", "medium": "https://YOUR-SSRF.onrender.com", "hard": "https://YOUR-SSRF.onrender.com"}},
    "xxe_lab": {"name": "XXE Labs", "links": {"easy": "https://YOUR-XXE.onrender.com", "medium": "https://YOUR-XXE.onrender.com", "hard": "https://YOUR-XXE.onrender.com"}},
    "csrf_lab": {"name": "CSRF Labs", "links": {"easy": "https://YOUR-CSRF.onrender.com", "medium": "https://YOUR-CSRF.onrender.com", "hard": "https://YOUR-CSRF.onrender.com"}}
}

@app.route('/')
def index(): return send_from_directory('.', 'index.html')

@app.route('/api/tools')
@limiter.limit("30 per minute")
def get_tools(): return jsonify(TOOLS_DB)

@app.route('/api/deploy', methods=['POST'])
@limiter.limit("20 per minute")
def deploy_lab():
    data = request.json
    tool = data.get('tool')
    diff = data.get('diff')
    
    if tool not in TOOLS_DB:
        return jsonify({"success": False})
        
    target_url = TOOLS_DB[tool]['links'].get(diff)
    fake_ip = f"10.10.{random.randint(1, 254)}.{random.randint(1, 254)}"
    
    return jsonify({"success": True, "url": target_url, "ip": fake_ip})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
