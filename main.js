
pdfjsLib.GlobalWorkerOptions.workerSrc = 'https://cdnjs.cloudflare.com/ajax/libs/pdf.js/3.11.174/pdf.worker.min.js';

let processedData = [];
let currentMode = "components";

const WHITELIST = [
"A1", "B1", "B2", "E1", "F1", "F2", "F3", "F4", "F5", "F6", "F7", "F8", "F9",
"H0.1", "H1", "H2", "H3", "H4", "H5", "H6", "H7", "H8", "H9", "H10", "H11",
"K0", "K1", "K2", "K3", "K4", "K5", "K6", "K7", "KA1", "KA2", "KA3", "KA4",
"KA5", "KA6", "KA7", "KA8", "KA9", "KA10", "KA11", "KA12", "KA13", "KA14",
"KA15", "KA16", "KA17", "KA18", "KA19", "KA20", "KA21", "KA22", "KA23", "KA24",
"KA25", "KA26", "KA27", "KA28", "KA29", "KA30", "KA31", "KA32", "KA33", "KA34",
"KA35", "KA36", "KA37", "KA38", "KA39", "KA40", "KA41", "KA42", "KA43", "KA44",
"KA45", "KA46", "KA47", "KA48", "P1", "Q0", "Q1", "Q2", "Q3", "Q4", "Q5", "Q6",
"Q7", "Q8", "Q9", "Q10", "S0.1", "S1", "S2", "S3", "S4", "S5", "S6", "S7",
"S8", "S9", "S10", "S11", "TX1", "X1", "X2", "X3", "XF3901", "XO"
];

const BLACKLIST = ['CREA', 'PARA', 'OUT', 'A'];

// --- FUNÇÕES DE FILTRAGEM E PROCESSAMENTO ---

function applyFilters(matches) {
    return matches.filter(item => {
    // 1. Regra da Blacklist: Descarta se estiver na lista
    if (BLACKLIST.includes(item)) {
    return false;
    }

    // 2. Regra da Whitelist: Se preenchida, aceita APENAS os itens dela
    if (WHITELIST.length > 0) {
    return WHITELIST.includes(item);
    }

    return true;
    });
}

// Modo 1: Extrai, Filtra e Ordena A-Z
function processComponents(text) {
    const pattern = /\b\d*[A-Z]{1,4}\d*\b/g;
    const rawMatches = text.match(pattern) || [];

    // Aplica Filtros
    const filteredMatches = applyFilters(rawMatches);

    // Ordena de A-Z a lista filtrada
    return filteredMatches.sort((a, b) => a.localeCompare(b, undefined, { numeric: true }));
}

// Modo 2: Extrai, Filtra, Duplica e Ordena A-Z
function processWires(text) {
    const pattern = /\b\d*[A-Z]{1,4}\d*\b/g;
    const rawMatches = text.match(pattern) || [];

    // Aplica Filtros
    const filteredMatches = applyFilters(rawMatches);

    // Duplica a lista FILTRADA
    const duplicated = [...filteredMatches, ...filteredMatches];

    // Ordena de A-Z
    return duplicated.sort((a, b) => a.localeCompare(b, undefined, { numeric: true }));
}

// --- FLUXO PRINCIPAL ---

async function processPDF() {
    const fileInput = document.getElementById('pdfInput');
    const startPageNum = parseInt(document.getElementById('startPage').value);
    const endPageNum = parseInt(document.getElementById('endPage').value);
    const output = document.getElementById('output');
    const btnDownload = document.getElementById('btnDownload');

    if (!fileInput.files[0]) {
    alert("Selecione um arquivo PDF primeiro!");
    return;
    }

    output.value = "Extraindo texto do PDF...";
    btnDownload.disabled = true;

    const file = fileInput.files[0];
    const arrayBuffer = await file.arrayBuffer();
    const pdf = await pdfjsLib.getDocument({ data: arrayBuffer }).promise;

    let extractedText = "";
    let start = startPageNum;
    let end = (endPageNum === 0 || endPageNum < startPageNum) ? startPageNum : endPageNum;

    if (start > pdf.numPages || end > pdf.numPages) {
    output.value = `ERRO: Intervalo fora do limite de páginas do PDF (Total: ${pdf.numPages})`;
    return;
    }

    for (let i = start; i <= end; i++) {
    const page = await pdf.getPage(i);
    const textContent = await page.getTextContent();
    extractedText += textContent.items.map(item => item.str).join(' ') + "\n";
    }

    const isWiresMode = document.getElementById('modeWires').checked;
    currentMode = isWiresMode ? "wires" : "components";

    if (isWiresMode) {
    processedData = processWires(extractedText);
    } else {
    processedData = processComponents(extractedText);
    }

    output.value = `Modo: ${currentMode.toUpperCase()} | Total de itens: ${processedData.length}\n\n` + processedData.join("\n");

    if (processedData.length > 0) {
    btnDownload.disabled = false;
    }
}

// --- GERADOR DE CSV ---

function downloadCSV() {
    if (processedData.length === 0) return;

    const header = currentMode === "wires" ? "Wire" : "Component";
    const csvContent = `${header}\n` + processedData.join("\n");

    const blob = new Blob(["\ufeff" + csvContent], { type: 'text/csv;charset=utf-8;' });

    const link = document.createElement("a");
    const url = URL.createObjectURL(blob);

    link.setAttribute("href", url);
    link.setAttribute("download", `extracao_${currentMode}.csv`);
    document.body.appendChild(link);

    link.click();

    document.body.removeChild(link);
    URL.revokeObjectURL(url);
}