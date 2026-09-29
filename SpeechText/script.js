function listen() {
  const inputArea = document.getElementById('input-area');
  const outputArea = document.getElementById('output-area');

  const recognition = new webkitSpeechRecognition();
  recognition.lang = "es-MX";        // o "es-ES"
  recognition.interimResults = false;
  recognition.maxAlternatives = 1;

  recognition.start();

  // Quita acentos/diacríticos, pasa a minúsculas y limpia símbolos
  function normalizeText(s) {
    return (s || "")
      .toLowerCase()
      .normalize("NFD")
      .replace(/[\u0300-\u036f]/g, "")        // quita acentos
      .replace(/[¿?¡!.,;:"]/g, "")            // quita signos comunes
      .replace(/\s+/g, " ")                   // colapsa espacios
      .trim();
  }

  // Detecta si el usuario está pidiendo la hora
  function isAskingForTime(rawTranscript) {
    const t = normalizeText(rawTranscript);

    // Frases comunes (puedes seguir agregando)
    const exactPhrases = new Set([
      "dame la hora",
      "dime la hora",
      "dime la hora exacta",
      "dime la hora exata",   // error común
      "que hora es",
      "que hora son",
      "hora",
      "la hora",
      "me dices la hora",
      "me puedes decir la hora",
      "me podrias decir la hora",
      "me podrías decir la hora",
      "podrias decirme la hora",
      "podrias darme la hora",
      "puedes decirme la hora",
      "puedes darme la hora",
      "me das la hora",
      "me dices la hora"
    ]);

    if (exactPhrases.has(t)) return true;

    // Reglas por intención (más flexible):
    // 1) si menciona "hora" o "qué hora"
    const mentionsHora =
      t.includes("hora") || t.includes("que hora");

    // 2) y además hay un verbo típico de pedir
    const askVerbs = [
      "dime", "dame", "di", "da",
      "decir", "dar",
      "puedes", "podrias", "podrías",
      "me dices", "me das",
      "me puedes", "me podrias", "me podrías"
    ];

    const hasAskVerb = askVerbs.some(v => t.includes(v));

    // Caso especial: si solo dicen "hora" o "la hora" ya lo aceptamos arriba,
    // pero también si dicen algo como "hora por favor"
    const softAsk = mentionsHora && (hasAskVerb || t.includes("por favor"));

    return softAsk;
  }

  function getSpanishTimeString({ withSeconds = true, use24h = true } = {}) {
    const now = new Date();
    return now.toLocaleTimeString("es-MX", {
      hour: "2-digit",
      minute: "2-digit",
      second: withSeconds ? "2-digit" : undefined,
      hour12: !use24h
    });
  }

  recognition.onresult = function (event) {
    const transcript = event.results[0][0].transcript;

    // (Opcional) mostrar lo que entendió
    if (inputArea) inputArea.value = transcript;

    if (isAskingForTime(transcript)) {
      const time = getSpanishTimeString({ withSeconds: true, use24h: true });
      outputArea.innerHTML = "La hora actual es: " + time;
    } else {
      // Si quieres, puedes dejarlo en silencio en vez de esto
      outputArea.innerHTML = "No entendí una solicitud de hora. Dijiste: " + transcript;
    }
  };

  recognition.onerror = function (e) {
    outputArea.innerHTML = "Error de reconocimiento de voz: " + (e.error || "desconocido");
  };
}