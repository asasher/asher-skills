// The browser surface. Univer owns cell editing; the side panel renders read-only previews of
// declared charts and pivots from the same snapshot + objects inputs used by the converter.
import { createUniver, LocaleType, mergeLocales } from '@univerjs/presets';
import { UniverSheetsConditionalFormattingPreset } from '@univerjs/preset-sheets-conditional-formatting';
import UniverPresetSheetsConditionalFormattingEnUS from '@univerjs/preset-sheets-conditional-formatting/locales/en-US';
import { UniverSheetsCorePreset } from '@univerjs/preset-sheets-core';
import UniverPresetSheetsCoreEnUS from '@univerjs/preset-sheets-core/locales/en-US';
import { UniverSheetsDataValidationPreset } from '@univerjs/preset-sheets-data-validation';
import UniverPresetSheetsDataValidationEnUS from '@univerjs/preset-sheets-data-validation/locales/en-US';

import '@univerjs/preset-sheets-conditional-formatting/lib/index.css';
import '@univerjs/preset-sheets-core/lib/index.css';
import '@univerjs/preset-sheets-data-validation/lib/index.css';

const SVG_NS = 'http://www.w3.org/2000/svg';
const CHART_COLORS = ['#2563eb', '#f97316', '#16a34a', '#dc2626', '#7c3aed', '#0891b2', '#ca8a04'];
const statusElement = document.getElementById('status');
const objectsPanel = document.getElementById('objects');

function setStatus(message, state = '') {
  statusElement.textContent = message;
  if (state) statusElement.dataset.state = state;
  else delete statusElement.dataset.state;
}

async function fetchJson(path) {
  const response = await fetch(path, { cache: 'no-store', headers: { Accept: 'application/json' } });
  if (!response.ok) throw new Error(`${path} returned HTTP ${response.status}`);
  return response.json();
}

let univerAPI;
let fWorkbook;

async function initialize() {
  let initialSnapshot = {};
  let loadError = null;
  try {
    initialSnapshot = await fetchJson('/snapshot');
  } catch (error) {
    loadError = error;
  }

  ({ univerAPI } = createUniver({
    locale: LocaleType.EN_US,
    locales: {
      [LocaleType.EN_US]: mergeLocales(
        UniverPresetSheetsCoreEnUS,
        UniverPresetSheetsConditionalFormattingEnUS,
        UniverPresetSheetsDataValidationEnUS,
      ),
    },
    presets: [
      UniverSheetsCorePreset({ container: 'app' }),
      UniverSheetsConditionalFormattingPreset(),
      UniverSheetsDataValidationPreset(),
    ],
  }));

  const workbookData = initialSnapshot && initialSnapshot.sheetOrder ? initialSnapshot : {};
  fWorkbook = univerAPI.createWorkbook(workbookData);
  setStatus(loadError ? `load failed: ${loadError.message}` : 'ready', loadError ? 'error' : '');

  // CommandExecuted fires on edits; guard the API shape across Univer versions.
  try {
    univerAPI.addEvent(univerAPI.Event.CommandExecuted, scheduleSave);
  } catch {
    setStatus('ready (manual save: window.saveWorkbook())');
  }

  void renderObjects();

  // Expose the Facade and explicit save/refresh hooks for agent-driven edits and debugging.
  window.univerAPI = univerAPI;
  window.fWorkbook = fWorkbook;
  window.saveWorkbook = saveWorkbook;
  window.renderObjects = renderObjects;
}

// Debounced autosave: on any command, wait for quiet, then atomically persist the saved snapshot.
let saveTimer = null;

async function responseError(response) {
  try {
    const payload = await response.json();
    return payload.error ? `: ${payload.error}` : '';
  } catch {
    return '';
  }
}

async function saveWorkbook() {
  try {
    const data = await Promise.resolve(fWorkbook.save());
    const response = await fetch('/save', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(data),
    });
    if (!response.ok) {
      throw new Error(`HTTP ${response.status}${await responseError(response)}`);
    }
    setStatus(`saved ${new Date().toLocaleTimeString()}`);
    void renderObjects();
  } catch (error) {
    console.error('Workbook save failed', error);
    setStatus(`save failed: ${error.message}`, 'error');
  }
}

function scheduleSave() {
  setStatus('editing…');
  clearTimeout(saveTimer);
  saveTimer = setTimeout(saveWorkbook, 800);
}

// ---- snapshot range helpers ---------------------------------------------------------------
function columnIndex(label) {
  let value = 0;
  for (const character of label.toUpperCase()) {
    value = value * 26 + character.charCodeAt(0) - 64;
  }
  return value - 1;
}

function parseReference(reference, fallbackSheet) {
  if (typeof reference !== 'string' || !reference.trim()) {
    throw new Error('Range reference is missing');
  }

  let address = reference.trim();
  let sheetName = fallbackSheet;
  const separator = address.lastIndexOf('!');
  if (separator >= 0) {
    sheetName = address.slice(0, separator).trim();
    address = address.slice(separator + 1).trim();
    if (sheetName.startsWith("'") && sheetName.endsWith("'")) {
      sheetName = sheetName.slice(1, -1).replaceAll("''", "'");
    }
  }

  const match = address.match(/^\$?([A-Za-z]+)\$?(\d+)(?::\$?([A-Za-z]+)\$?(\d+))?$/);
  if (!match) throw new Error(`Invalid A1 range: ${reference}`);

  const startRow = Number(match[2]) - 1;
  const startColumn = columnIndex(match[1]);
  const endRow = Number(match[4] || match[2]) - 1;
  const endColumn = columnIndex(match[3] || match[1]);
  return {
    sheetName,
    startRow: Math.min(startRow, endRow),
    endRow: Math.max(startRow, endRow),
    startColumn: Math.min(startColumn, endColumn),
    endColumn: Math.max(startColumn, endColumn),
  };
}

function getSheet(snapshot, sheetName) {
  const sheets = Object.values(snapshot?.sheets || {});
  return sheets.find((sheet) => sheet.name === sheetName);
}

function getCellValue(sheet, row, column) {
  const cell = sheet?.cellData?.[String(row)]?.[String(column)];
  return cell && Object.prototype.hasOwnProperty.call(cell, 'v') ? cell.v : null;
}

function readRange(snapshot, reference, fallbackSheet) {
  const parsed = parseReference(reference, fallbackSheet);
  if (!parsed.sheetName) throw new Error(`Range has no sheet: ${reference}`);
  const sheet = getSheet(snapshot, parsed.sheetName);
  if (!sheet) throw new Error(`Sheet not found: ${parsed.sheetName}`);

  const matrix = [];
  for (let row = parsed.startRow; row <= parsed.endRow; row += 1) {
    const values = [];
    for (let column = parsed.startColumn; column <= parsed.endColumn; column += 1) {
      values.push(getCellValue(sheet, row, column));
    }
    matrix.push(values);
  }
  return { matrix, sheetName: parsed.sheetName };
}

function flatten(matrix) {
  return matrix.flatMap((row) => row);
}

function matrixColumns(matrix) {
  const width = Math.max(0, ...matrix.map((row) => row.length));
  return Array.from({ length: width }, (_, column) => matrix.map((row) => row[column] ?? null));
}

function numeric(value) {
  return typeof value === 'number' && Number.isFinite(value) ? value : null;
}

// ---- DOM + SVG helpers --------------------------------------------------------------------
function element(tag, className = '', text = '') {
  const node = document.createElement(tag);
  if (className) node.className = className;
  if (text !== '') node.textContent = text;
  return node;
}

function svgElement(tag, attributes = {}) {
  const node = document.createElementNS(SVG_NS, tag);
  for (const [name, value] of Object.entries(attributes)) node.setAttribute(name, String(value));
  return node;
}

function svgText(svg, text, x, y, className = 'chart-label', anchor = 'start') {
  const node = svgElement('text', { x, y, class: className, 'text-anchor': anchor });
  node.textContent = text;
  svg.append(node);
  return node;
}

function titledShape(node, label) {
  const title = svgElement('title');
  title.textContent = label;
  node.append(title);
  return node;
}

function shortNumber(value) {
  return new Intl.NumberFormat(undefined, { notation: 'compact', maximumFractionDigits: 1 }).format(value);
}

function displayValue(value) {
  if (value === null || value === undefined || value === '') return '—';
  if (typeof value === 'number') {
    return new Intl.NumberFormat(undefined, { maximumFractionDigits: 6 }).format(value);
  }
  if (typeof value === 'boolean') return value ? 'TRUE' : 'FALSE';
  return String(value);
}

function truncate(value, length = 11) {
  const text = displayValue(value);
  return text.length > length ? `${text.slice(0, length - 1)}…` : text;
}

function baseSvg(label) {
  return svgElement('svg', {
    viewBox: '0 0 400 210',
    class: 'chart-preview',
    role: 'img',
    'aria-label': label,
  });
}

function yScale(value, minimum, maximum, top = 12, height = 148) {
  return top + ((maximum - value) / (maximum - minimum)) * height;
}

function drawGrid(svg, minimum, maximum, left = 40, top = 12, width = 260, height = 148) {
  for (let index = 0; index <= 4; index += 1) {
    const y = top + (height * index) / 4;
    const value = maximum - ((maximum - minimum) * index) / 4;
    svg.append(svgElement('line', { x1: left, y1: y, x2: left + width, y2: y, class: 'chart-grid' }));
    svgText(svg, shortNumber(value), left - 5, y + 3, 'chart-label', 'end');
  }
  svg.append(svgElement('line', { x1: left, y1: top, x2: left, y2: top + height, class: 'chart-axis' }));
  svg.append(svgElement('line', { x1: left, y1: top + height, x2: left + width, y2: top + height, class: 'chart-axis' }));
}

function drawCategoryLabels(svg, categories, count, position) {
  const every = Math.max(1, Math.ceil(count / 10));
  for (let index = 0; index < count; index += every) {
    const text = svgText(svg, truncate(categories[index] ?? index + 1), position(index), 176, 'chart-label', 'middle');
    const title = svgElement('title');
    title.textContent = displayValue(categories[index] ?? index + 1);
    text.append(title);
  }
}

function drawSeriesLegend(svg, series, x = 311, y = 20) {
  const visible = series.slice(0, 7);
  visible.forEach((item, index) => {
    const rowY = y + index * 16;
    svg.append(svgElement('rect', {
      x,
      y: rowY - 8,
      width: 9,
      height: 9,
      rx: 1,
      fill: CHART_COLORS[index % CHART_COLORS.length],
    }));
    svgText(svg, truncate(item.title, 13), x + 14, rowY, 'chart-legend');
  });
  if (series.length > visible.length) {
    svgText(svg, `+${series.length - visible.length} more`, x, y + visible.length * 16, 'chart-legend');
  }
}

function chartDomain(series, includeZero) {
  const values = series.flatMap((item) => item.values).filter((value) => value !== null);
  if (!values.length) throw new Error('Chart ranges contain no numeric values');
  let minimum = Math.min(...values);
  let maximum = Math.max(...values);
  if (includeZero) {
    minimum = Math.min(0, minimum);
    maximum = Math.max(0, maximum);
  }
  if (minimum === maximum) {
    const padding = Math.abs(minimum) * 0.1 || 1;
    minimum -= padding;
    maximum += padding;
  }
  return { minimum, maximum };
}

function barChartSvg(chart, categories, series) {
  const svg = baseSvg(`${chart.title || chart.id || 'Declared'} bar chart`);
  const { minimum, maximum } = chartDomain(series, true);
  const left = 40;
  const top = 12;
  const width = 260;
  const height = 148;
  const count = Math.max(categories.length, ...series.map((item) => item.values.length));
  const groupWidth = width / Math.max(1, count);
  const barWidth = Math.max(1, (groupWidth * 0.74) / Math.max(1, series.length));
  const zeroY = yScale(0, minimum, maximum, top, height);
  drawGrid(svg, minimum, maximum, left, top, width, height);

  series.forEach((item, seriesIndex) => {
    item.values.forEach((value, index) => {
      if (value === null) return;
      const valueY = yScale(value, minimum, maximum, top, height);
      const rect = svgElement('rect', {
        x: left + index * groupWidth + groupWidth * 0.13 + seriesIndex * barWidth,
        y: Math.min(valueY, zeroY),
        width: barWidth,
        height: Math.max(0.75, Math.abs(zeroY - valueY)),
        fill: CHART_COLORS[seriesIndex % CHART_COLORS.length],
      });
      svg.append(titledShape(rect, `${displayValue(categories[index] ?? index + 1)} · ${item.title}: ${displayValue(value)}`));
    });
  });

  drawCategoryLabels(svg, categories, count, (index) => left + (index + 0.5) * groupWidth);
  drawSeriesLegend(svg, series);
  return svg;
}

function lineChartSvg(chart, categories, series) {
  const svg = baseSvg(`${chart.title || chart.id || 'Declared'} line chart`);
  const { minimum, maximum } = chartDomain(series, false);
  const left = 40;
  const top = 12;
  const width = 260;
  const height = 148;
  const count = Math.max(categories.length, ...series.map((item) => item.values.length));
  const x = (index) => left + (count === 1 ? width / 2 : (index * width) / (count - 1));
  drawGrid(svg, minimum, maximum, left, top, width, height);

  series.forEach((item, seriesIndex) => {
    let path = '';
    item.values.forEach((value, index) => {
      if (value === null) return;
      const point = `${x(index)} ${yScale(value, minimum, maximum, top, height)}`;
      path += `${index > 0 && item.values[index - 1] !== null ? ' L' : ' M'}${point}`;
    });
    svg.append(svgElement('path', {
      d: path,
      fill: 'none',
      stroke: CHART_COLORS[seriesIndex % CHART_COLORS.length],
      'stroke-width': 2,
    }));
    if (item.values.length <= 40) {
      item.values.forEach((value, index) => {
        if (value === null) return;
        const circle = svgElement('circle', {
          cx: x(index),
          cy: yScale(value, minimum, maximum, top, height),
          r: 2.5,
          fill: CHART_COLORS[seriesIndex % CHART_COLORS.length],
        });
        svg.append(titledShape(circle, `${displayValue(categories[index] ?? index + 1)} · ${item.title}: ${displayValue(value)}`));
      });
    }
  });

  drawCategoryLabels(svg, categories, count, x);
  drawSeriesLegend(svg, series);
  return svg;
}

function polarPoint(centerX, centerY, radius, angle) {
  return [centerX + radius * Math.cos(angle), centerY + radius * Math.sin(angle)];
}

function pieChartSvg(chart, categories, series) {
  const svg = baseSvg(`${chart.title || chart.id || 'Declared'} pie chart`);
  const values = series[0].values.map((value) => (value !== null && value > 0 ? value : 0));
  const total = values.reduce((sum, value) => sum + value, 0);
  if (!total) throw new Error('Pie chart range contains no positive numeric values');
  const centerX = 105;
  const centerY = 83;
  const radius = 66;
  let angle = -Math.PI / 2;

  values.forEach((value, index) => {
    if (!value) return;
    const nextAngle = angle + (value / total) * Math.PI * 2;
    const color = CHART_COLORS[index % CHART_COLORS.length];
    let shape;
    if (value === total) {
      shape = svgElement('circle', { cx: centerX, cy: centerY, r: radius, fill: color });
    } else {
      const [startX, startY] = polarPoint(centerX, centerY, radius, angle);
      const [endX, endY] = polarPoint(centerX, centerY, radius, nextAngle);
      const largeArc = nextAngle - angle > Math.PI ? 1 : 0;
      shape = svgElement('path', {
        d: `M ${centerX} ${centerY} L ${startX} ${startY} A ${radius} ${radius} 0 ${largeArc} 1 ${endX} ${endY} Z`,
        fill: color,
        stroke: '#fff',
        'stroke-width': 1,
      });
    }
    svg.append(titledShape(shape, `${displayValue(categories[index] ?? index + 1)}: ${displayValue(value)}`));
    angle = nextAngle;
  });

  const visible = values.map((value, index) => ({ value, index })).filter(({ value }) => value > 0).slice(0, 8);
  visible.forEach(({ value, index }, legendIndex) => {
    const y = 22 + legendIndex * 18;
    svg.append(svgElement('rect', {
      x: 205,
      y: y - 9,
      width: 10,
      height: 10,
      rx: 1,
      fill: CHART_COLORS[index % CHART_COLORS.length],
    }));
    svgText(svg, `${truncate(categories[index] ?? index + 1, 13)} · ${shortNumber(value)}`, 220, y, 'chart-legend');
  });
  if (series.length > 1) {
    svgText(svg, `Pie preview uses first series: ${truncate(series[0].title, 19)}`, 205, 190, 'chart-label');
  }
  return svg;
}

function chartSeries(snapshot, chart) {
  const series = [];
  for (const reference of Array.isArray(chart.values) ? chart.values : []) {
    const { matrix } = readRange(snapshot, reference, chart.sheet);
    const columns = matrixColumns(matrix);
    columns.forEach((values, column) => {
      const index = series.length;
      series.push({
        title: chart.seriesTitles?.[index] || (columns.length > 1 ? `${reference} [${column + 1}]` : reference),
        values: values.map(numeric),
      });
    });
  }
  if (!series.length) throw new Error('Chart has no value ranges');
  return series;
}

function renderChart(chart, snapshot, index) {
  const card = element('section', 'object-card');
  card.append(element('h3', 'object-title', `CHART · ${chart.title || chart.id || index + 1}`));
  card.append(element('p', 'object-meta', `${chart.type || 'bar'} · ${chart.sheet || 'unknown sheet'}!${chart.anchor || 'H2'}`));
  try {
    const series = chartSeries(snapshot, chart);
    const categories = chart.categories
      ? flatten(readRange(snapshot, chart.categories, chart.sheet).matrix)
      : Array.from({ length: Math.max(...series.map((item) => item.values.length)) }, (_, itemIndex) => itemIndex + 1);
    const declaredType = String(chart.type || 'bar').toLowerCase();
    const type = ['bar', 'line', 'pie'].includes(declaredType) ? declaredType : 'bar';
    const svg = type === 'line'
      ? lineChartSvg(chart, categories, series)
      : type === 'pie'
        ? pieChartSvg(chart, categories, series)
        : barChartSvg(chart, categories, series);
    card.append(svg);
    if (type !== declaredType) {
      card.append(element('p', 'object-note', `Unknown chart type “${declaredType}”; previewed as the converter's bar fallback.`));
    }

    const references = [chart.categories, ...(Array.isArray(chart.values) ? chart.values : [])].filter(Boolean);
    const crossSheet = references.some((reference) => parseReference(reference, chart.sheet).sheetName !== chart.sheet);
    if (crossSheet) {
      card.append(element('p', 'object-note', 'Cross-sheet ranges are resolved for this preview; the current converter requires same-sheet chart declarations.'));
    }
  } catch (error) {
    card.append(element('p', 'object-error', `Preview unavailable: ${error.message}`));
  }
  return card;
}

// ---- pivot preview ------------------------------------------------------------------------
function valueKey(values) {
  return JSON.stringify(values.map((value) => [typeof value, value]));
}

function compareKeys(left, right) {
  return left.map(displayValue).join('\u0000').localeCompare(
    right.map(displayValue).join('\u0000'),
    undefined,
    { numeric: true, sensitivity: 'base' },
  );
}

function newAggregateState() {
  return { sum: 0, count: 0, countA: 0, min: null, max: null, product: 1, distinct: new Set() };
}

function accumulate(state, value) {
  if (value !== null && value !== undefined && value !== '') {
    state.countA += 1;
    state.distinct.add(valueKey([value]));
  }
  const number = numeric(value);
  if (number === null) return;
  state.sum += number;
  state.count += 1;
  state.min = state.min === null ? number : Math.min(state.min, number);
  state.max = state.max === null ? number : Math.max(state.max, number);
  state.product *= number;
}

function normalizedAgg(agg) {
  return String(agg || 'sum').toLowerCase().replace(/[\s_-]/g, '');
}

function aggregateResult(state, agg) {
  switch (normalizedAgg(agg)) {
    case 'sum': return state.sum;
    case 'count': return state.count;
    case 'counta': return state.countA;
    case 'average':
    case 'avg': return state.count ? state.sum / state.count : null;
    case 'min': return state.min;
    case 'max': return state.max;
    case 'product': return state.count ? state.product : null;
    case 'distinctcount': return state.distinct.size;
    default: throw new Error(`Unsupported pivot aggregation: ${agg}`);
  }
}

function states(count) {
  return Array.from({ length: count }, newAggregateState);
}

function addRowToStates(target, row, fieldIndexes) {
  target.forEach((state, index) => accumulate(state, row[fieldIndexes[index]]));
}

function pivotTable(snapshot, pivot) {
  const { matrix } = readRange(snapshot, pivot.source);
  if (!matrix.length) throw new Error('Pivot source is empty');
  const headers = matrix[0].map((value) => String(value ?? ''));
  const rowFields = Array.isArray(pivot.rows) ? pivot.rows : [];
  const columnFields = Array.isArray(pivot.cols) ? pivot.cols : [];
  const valueSpecs = Array.isArray(pivot.values) ? pivot.values : [];
  if (!valueSpecs.length) throw new Error('Pivot has no value fields');
  valueSpecs.forEach((spec) => aggregateResult(newAggregateState(), spec.agg));

  const fieldIndex = (field) => {
    const index = headers.indexOf(String(field));
    if (index < 0) throw new Error(`Pivot field not found: ${field}`);
    return index;
  };
  const rowIndexes = rowFields.map(fieldIndex);
  const columnIndexes = columnFields.map(fieldIndex);
  const valueIndexes = valueSpecs.map((spec) => fieldIndex(spec.field));
  const rowKeys = new Map();
  const columnKeys = new Map();
  const grouped = new Map();
  const rowTotals = new Map();
  const columnTotals = new Map();
  const grandTotals = states(valueSpecs.length);

  for (const row of matrix.slice(1)) {
    const rowValues = rowIndexes.map((index) => row[index]);
    const columnValues = columnIndexes.map((index) => row[index]);
    const rowId = valueKey(rowValues);
    const columnId = valueKey(columnValues);
    rowKeys.set(rowId, rowValues);
    columnKeys.set(columnId, columnValues);

    if (!grouped.has(rowId)) grouped.set(rowId, new Map());
    const rowGroups = grouped.get(rowId);
    if (!rowGroups.has(columnId)) rowGroups.set(columnId, states(valueSpecs.length));
    if (!rowTotals.has(rowId)) rowTotals.set(rowId, states(valueSpecs.length));
    if (!columnTotals.has(columnId)) columnTotals.set(columnId, states(valueSpecs.length));
    addRowToStates(rowGroups.get(columnId), row, valueIndexes);
    addRowToStates(rowTotals.get(rowId), row, valueIndexes);
    addRowToStates(columnTotals.get(columnId), row, valueIndexes);
    addRowToStates(grandTotals, row, valueIndexes);
  }

  if (!rowKeys.size) {
    const emptyId = valueKey([]);
    rowKeys.set(emptyId, []);
    columnKeys.set(emptyId, []);
    grouped.set(emptyId, new Map([[emptyId, states(valueSpecs.length)]]));
    rowTotals.set(emptyId, states(valueSpecs.length));
    columnTotals.set(emptyId, states(valueSpecs.length));
  }

  const sortedRows = [...rowKeys.entries()].sort((left, right) => compareKeys(left[1], right[1]));
  const sortedColumns = [...columnKeys.entries()].sort((left, right) => compareKeys(left[1], right[1]));
  const table = element('table', 'pivot-preview');
  const thead = element('thead');
  const headerRow = element('tr');
  const displayedRowFields = rowFields.length ? rowFields : ['Group'];
  displayedRowFields.forEach((field) => headerRow.append(element('th', '', field)));

  const aggregateLabel = (spec) => `${normalizedAgg(spec.agg)}(${spec.field})`;
  for (const [, columnValues] of sortedColumns) {
    for (const spec of valueSpecs) {
      const prefix = columnFields.length ? `${columnValues.map(displayValue).join(' · ')} · ` : '';
      headerRow.append(element('th', '', `${prefix}${aggregateLabel(spec)}`));
    }
  }
  if (columnFields.length) {
    valueSpecs.forEach((spec) => headerRow.append(element('th', '', `Total · ${aggregateLabel(spec)}`)));
  }
  thead.append(headerRow);
  table.append(thead);

  const tbody = element('tbody');
  for (const [rowId, rowValues] of sortedRows) {
    const tr = element('tr');
    const displayedValues = rowFields.length ? rowValues : ['All'];
    displayedValues.forEach((value) => tr.append(element('td', '', displayValue(value))));
    const rowGroups = grouped.get(rowId);
    for (const [columnId] of sortedColumns) {
      const groupStates = rowGroups?.get(columnId) || states(valueSpecs.length);
      valueSpecs.forEach((spec, valueIndex) => {
        tr.append(element('td', '', displayValue(aggregateResult(groupStates[valueIndex], spec.agg))));
      });
    }
    if (columnFields.length) {
      valueSpecs.forEach((spec, valueIndex) => {
        tr.append(element('td', '', displayValue(aggregateResult(rowTotals.get(rowId)[valueIndex], spec.agg))));
      });
    }
    tbody.append(tr);
  }

  const grandRow = element('tr', 'grand-total');
  displayedRowFields.forEach((_, index) => grandRow.append(element('td', '', index === 0 ? 'Grand Total' : '')));
  for (const [columnId] of sortedColumns) {
    valueSpecs.forEach((spec, valueIndex) => {
      grandRow.append(element('td', '', displayValue(aggregateResult(columnTotals.get(columnId)[valueIndex], spec.agg))));
    });
  }
  if (columnFields.length) {
    valueSpecs.forEach((spec, valueIndex) => {
      grandRow.append(element('td', '', displayValue(aggregateResult(grandTotals[valueIndex], spec.agg))));
    });
  }
  tbody.append(grandRow);
  table.append(tbody);
  return table;
}

function renderPivot(pivot, snapshot, index) {
  const card = element('section', 'object-card');
  card.append(element('h3', 'object-title', `PIVOT · ${pivot.id || index + 1}`));
  const rows = Array.isArray(pivot.rows) && pivot.rows.length ? pivot.rows.join(' + ') : '(all rows)';
  const columns = Array.isArray(pivot.cols) && pivot.cols.length ? ` × ${pivot.cols.join(' + ')}` : '';
  card.append(element('p', 'object-meta', `${rows}${columns} · ${pivot.source || 'missing source'} → ${pivot.sheet || 'unknown sheet'}!${pivot.anchor || 'A1'} · static on compile`));
  try {
    const scroll = element('div', 'preview-scroll');
    scroll.append(pivotTable(snapshot, pivot));
    card.append(scroll);
    const hasColumns = Array.isArray(pivot.cols) && pivot.cols.length > 0;
    const hasNonSum = Array.isArray(pivot.values)
      && pivot.values.some((spec) => normalizedAgg(spec.agg) !== 'sum');
    if (hasColumns || hasNonSum) {
      card.append(element('p', 'object-note', 'Preview honors the declared columns and aggregations; the current Tier A converter is exactly equivalent only for row-grouped sums.'));
    }
  } catch (error) {
    card.append(element('p', 'object-error', `Preview unavailable: ${error.message}`));
  }
  return card;
}

// ---- declared-object panel ---------------------------------------------------------------
let renderGeneration = 0;

async function renderObjects() {
  const generation = ++renderGeneration;
  try {
    const [objects, snapshot] = await Promise.all([fetchJson('/objects'), fetchJson('/snapshot')]);
    if (generation !== renderGeneration) return;
    const charts = Array.isArray(objects.charts) ? objects.charts : [];
    const pivots = Array.isArray(objects.pivots) ? objects.pivots : [];
    objectsPanel.replaceChildren();
    if (!charts.length && !pivots.length) {
      objectsPanel.hidden = true;
      return;
    }

    objectsPanel.hidden = false;
    objectsPanel.append(element('h2', 'objects-heading', `Declared objects (${charts.length + pivots.length})`));
    charts.forEach((chart, index) => objectsPanel.append(renderChart(chart, snapshot, index)));
    pivots.forEach((pivot, index) => objectsPanel.append(renderPivot(pivot, snapshot, index)));
  } catch (error) {
    if (generation !== renderGeneration) return;
    objectsPanel.hidden = false;
    objectsPanel.replaceChildren(
      element('h2', 'objects-heading', 'Declared objects'),
      element('p', 'object-error', `Preview load failed: ${error.message}`),
    );
  }
}

void initialize();
