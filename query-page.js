/// Configurações Iniciais ///
////////////////////////////////////////////////////

const initialSettings = {
  vaultName: "Meu Vault",
  queryPath: "",
  initialNameFilter: "",
  dynamicColumnProperties: {
    "Nome da Nota": "name.obsidian",
    "HUB": "hub",
    "Connections": "connections",
    "Created": "created",
    "Tags": "tags",
  },
  groupByColumns: [],
  pagination: {
    isEnabled: true,
    itemsPerPage: 10,
  },
  viewHeight: "900px",
  placeholders: {
    nameFilter: "Pesquisa Geral...",
    queryPath: "Caminho da nota...",
    headerTitle: "Buscar Notas",
    newHeaderLabel: "Novo Cabeçalho",
    newDataField: "Novo Campo",
  },
  excludedFolders: ["+", "SYSTEM", "ATLAS/MOCS", "CALENDAR"],
};

/// Funções Auxiliares ///
////////////////////////////////////////////////////

const { useState, useMemo } = dc;

function getProperty(entry, property) {
  if (!entry) return [""];

  // Handle Obsidian-specific properties
  if (property.endsWith(".obsidian")) {
    const key = property.replace(".obsidian", "");
    const obsidianProps = {
      ctime: entry.$ctime?.toISODate?.() ?? "",
      mtime: entry.$mtime?.toISODate?.() ?? "",
      name: entry.$name ?? "",
    };
    return [obsidianProps[key] ?? ""];
  }
	
	if (property === "created") {
	  const createdDate = entry.$ctime?.toISODate?.() ?? "";
	  return [`[[${createdDate}]]`];
	}


  // Handle tags - formato #tag clicável
  if (property === "tags") {
    if (entry.$tags?.length) {
      return entry.$tags.map(tag => tag.startsWith("#") ? tag : `#${tag}`);
    }
    return [""];
  }

  // Handle HUB and Connections properties
  if (property === "hub" || property === "connections") {
    const frontmatterField = entry.$frontmatter?.[property];
    
    if (frontmatterField === undefined || frontmatterField === null || frontmatterField === "") {
      return [""];
    }

    // Handle array values
    if (Array.isArray(frontmatterField)) {
      return frontmatterField.map(item => {
        if (typeof item === 'string' && item.match(/^\[\[.*\]\]$/)) {
          return item;
        }
        if (typeof item === 'object' && item.path) {
          return `[[${item.path}]]`;
        }
        return `[[${cleanLink(item)}]]`;
      });
    }

    // Handle single string values
    if (typeof frontmatterField === 'string') {
      if (frontmatterField.match(/^\[\[.*\]\]$/)) {
        return [frontmatterField];
      }
      return [`[[${cleanLink(frontmatterField)}]]`];
    }

    // Handle object with raw array
    if (typeof frontmatterField === 'object' && frontmatterField.raw && Array.isArray(frontmatterField.raw)) {
      return frontmatterField.raw.map(item => {
        if (typeof item === 'string' && item.match(/^\[\[.*\]\]$/)) {
          return item;
        }
        return `[[${cleanLink(item)}]]`;
      });
    }

    // Handle single object with path
    if (typeof frontmatterField === 'object' && frontmatterField.path) {
      return [`[[${frontmatterField.path}]]`];
    }

    // Default case for other objects
    if (typeof frontmatterField === 'object') {
      return [""];
    }

    // Fallback
    return [`[[${cleanLink(String(frontmatterField))}]]` || ""];
  }

  return [""];
}

function cleanLink(value) {
  if (value === null || value === undefined) return "";
  const str = String(value).trim();
  const match = str.match(/\[\[(.*?)\]\]/);
  return match ? match[1].trim() : str;
}

/// Estilos ///
////////////////////////////////////////////////////

const styles = {
  mainContainer: {
    display: "flex",
    flexDirection: "column",
    backgroundColor: "var(--background-primary)",
    color: "var(--text-normal)",
    height: "100%",
  },
  header: {
    padding: "10px",
    backgroundColor: "var(--background-primary)",
  },
  headerTitle: {
    margin: 0,
    paddingBottom: "10px",
  },
  controlGroup: {
    display: "flex",
    gap: "10px",
    flexWrap: "wrap",
    alignItems: "center",
  },
  textbox: {
    padding: "8px",
    border: "1px solid var(--background-modifier-border)",
    backgroundColor: "var(--background-primary)",
    color: "var(--text-normal)",
    width: "200px",
    boxSizing: "border-box",
  },
  tableContainer: {
    flex: 1,
    overflowY: "auto",
  },
  tableHeader: {
    display: "flex",
    backgroundColor: "var(--background-primary)",
    position: "sticky",
    top: 0,
    zIndex: 2,
  },
  tableHeaderCell: {
    flex: 1,
    padding: "10px",
    fontWeight: "bold",
    borderBottom: "1px solid var(--background-modifier-border)",
    display: "flex",
    flexDirection: "column",
    gap: "5px",
  },
  columnFilter: {
    padding: "4px",
    border: "1px solid var(--background-modifier-border)",
    backgroundColor: "var(--background-primary)",
    color: "var(--text-normal)",
    width: "100%",
    boxSizing: "border-box",
    fontSize: "0.9em",
  },
  tableRow: {
    display: "flex",
    borderBottom: "1px solid var(--background-modifier-border)",
  },
  tableCell: {
    flex: 1,
    padding: "10px",
    display: "flex",
    flexDirection: "column",
    gap: "4px",
  },
  draggableLink: {
    cursor: "pointer",
    color: "var(--text-accent)",
  },
  pagination: {
    padding: "30px",
    display: "flex",
    justifyContent: "center",
    gap: "10px",
    borderBottom: "20%",
  },
  button: {
    padding: "8px 12px",
    backgroundColor: "var(--interactive-accent)",
    color: "var(--text-on-accent)",
    border: "none",
    borderRadius: "4px",
    cursor: "pointer",
  },
  tagContainer: {
    display: "flex",
    flexDirection: "column",
    gap: "4px",
  },
  tag: {
    display: "inline-block",
    color: "var(--text-accent)",
    fontSize: "0.9em",
    whiteSpace: "nowrap",
    cursor: "pointer",
    textDecoration: "none",
    '&:hover': {
      textDecoration: "underline",
    }
  },
  arrayItem: {
    padding: "2px 0",
  },
  dateCell: {
    fontSize: "0.9em",
    color: "var(--text-muted)",
  },
};

////////////////////////////////////////////////////
/// Componentes ///
////////////////////////////////////////////////////

function NoteLink({ entry }) {
  const title = getProperty(entry, "name.obsidian")[0];
  return title ? (
    <a
      href="#"
      className="internal-link"
      draggable
      data-href={entry.$path}
      style={styles.draggableLink}
    >
      {title}
    </a>
  ) : null;
}

function Tags({ values }) {
  const filteredValues = values.filter(val => val !== "");
  if (filteredValues.length === 0) return null;
  return (
    <div style={styles.tagContainer}>
      {filteredValues.map((val, idx) => {
        const tagName = val.startsWith("#") ? val.slice(1) : val;
        return (
          <a
            key={idx}
            href="#"
            className="tag"
            data-href={`#${tagName}`}
            style={styles.tag}
            onClick={(e) => {
              e.preventDefault();
              if (window.app?.internalPlugins?.plugins?.tags?.instance?.navigateToTag) {
                window.app.internalPlugins.plugins.tags.instance.navigateToTag(tagName);
              }
            }}
          >
            {val}
          </a>
        );
      })}
    </div>
  );
}

function ArrayItems({ values, isDate = false }) {
  const filteredValues = values.filter(val => val !== "");
  if (filteredValues.length === 0) return null;
  
  return (
    <div style={styles.tagContainer}>
      {filteredValues.map((val, idx) => {
        const isMarkdownLink = typeof val === 'string' && val.startsWith("[[") && val.endsWith("]]");
        const linkText = isMarkdownLink ? val.slice(2, -2) : val;
        
        return (
          <div key={idx} style={isDate ? styles.dateCell : styles.arrayItem}>
            {isMarkdownLink ? (
              <a
                href="#"
                className="internal-link"
                data-href={linkText}
                style={styles.draggableLink}
              >
                {linkText}
              </a>
            ) : (
              linkText
            )}
          </div>
        );
      })}
    </div>
  );
}

function DataTable({ columns, data, columnFilters, setColumnFilter }) {
  return (
    <div style={styles.tableContainer}>
      <div style={styles.tableHeader}>
        {columns.map(col => {
          const property = initialSettings.dynamicColumnProperties[col];
          return (
            <div key={col} style={styles.tableHeaderCell}>
              <div>{col}</div>
              <input
                type="text"
                value={columnFilters[col] || ""}
                onChange={e => setColumnFilter(col, e.target.value)}
                placeholder={`Filtrar ${col.toLowerCase()}...`}
                style={styles.columnFilter}
              />
            </div>
          );
        })}
      </div>
      <div>
        {data.length === 0 && (
          <div style={{ padding: "10px", textAlign: "center" }}>Nenhuma nota encontrada</div>
        )}
        {data.map((entry, idx) => (
          <div key={idx} style={styles.tableRow}>
            {columns.map(col => {
              const property = initialSettings.dynamicColumnProperties[col];
              const values = getProperty(entry, property);
              
              return (
                <div key={`${idx}-${col}`} style={styles.tableCell}>
                  {property === "name.obsidian" ? (
                    <NoteLink entry={entry} />
                  ) : property === "tags" ? (
                    <Tags values={values} />
                  ) : property === "created" ? (
                    <ArrayItems values={values} isDate={true} />
                  ) : (
                    <ArrayItems values={values} />
                  )}
                </div>
              );
            })}
          </div>
        ))}
      </div>
    </div>
  );
}

function Pagination({ currentPage, totalPages, setCurrentPage }) {
  return (
    <div style={styles.pagination}>
      <button
        style={styles.button}
        disabled={currentPage === 1}
        onClick={() => setCurrentPage(p => Math.max(1, p - 1))}
      >
        Anterior
      </button>
      <span>Página {currentPage} de {totalPages}</span>
      <button
        style={styles.button}
        disabled={currentPage === totalPages}
        onClick={() => setCurrentPage(p => Math.min(totalPages, p + 1))}
      >
        Próxima
      </button>
    </div>
  );
}

////////////////////////////////////////////////////
/// Componente Principal ///
////////////////////////////////////////////////////

function View() {
  const [nameFilter, setNameFilter] = useState(initialSettings.initialNameFilter);
  const [queryPath, setQueryPath] = useState(initialSettings.queryPath);
  const [currentPage, setCurrentPage] = useState(1);
  const [columnFilters, setColumnFilters] = useState({});

  const qdata = dc.useQuery(`@page and path("${queryPath}")`);

  const setColumnFilter = (column, value) => {
    setColumnFilters(prev => ({
      ...prev,
      [column]: value
    }));
    setCurrentPage(1);
  };

  const filteredData = useMemo(() => {
    const searchTerm = nameFilter.trim().toLowerCase();
    const activeColumns = Object.keys(initialSettings.dynamicColumnProperties);

    return qdata.filter(entry => {
      const isExcluded = initialSettings.excludedFolders.some(folder =>
        entry.$path.startsWith(`${folder}/`)
      );
      if (isExcluded) return false;

      const matchesGlobalFilter = searchTerm === "" ||
        activeColumns.some(col => {
          const prop = initialSettings.dynamicColumnProperties[col];
          const value = getProperty(entry, prop).join(", ").toLowerCase();
          return value.includes(searchTerm);
        });

      if (!matchesGlobalFilter) return false;

      return activeColumns.every(col => {
        const filterValue = columnFilters[col]?.trim().toLowerCase();
        if (!filterValue) return true;

        const prop = initialSettings.dynamicColumnProperties[col];
        const values = getProperty(entry, prop);
        
        if (prop === "tags") {
          return values.some(tag =>
            tag.replace('#', '').toLowerCase().includes(filterValue)
          );
        }
        
        if (prop === "created") {
          return values.some(date =>
            date.toLowerCase().includes(filterValue)
          );
        }
        
        return values.some(value =>
          value.toLowerCase().includes(filterValue)
        );
      });
    });
  }, [qdata, nameFilter, columnFilters]);

  const paginatedData = useMemo(() => {
    const start = (currentPage - 1) * initialSettings.pagination.itemsPerPage;
    const end = start + initialSettings.pagination.itemsPerPage;
    return filteredData.slice(start, end);
  }, [filteredData, currentPage]);

  const totalPages = Math.max(1, Math.ceil(filteredData.length / initialSettings.pagination.itemsPerPage));

  const columns = Object.keys(initialSettings.dynamicColumnProperties);

  return (
    <div style={{...styles.mainContainer, height: initialSettings.viewHeight}}>
      <div style={styles.header}>
        <h1 style={styles.headerTitle}>{initialSettings.placeholders.headerTitle}</h1>
        <div style={styles.controlGroup}>
          <dc.Textbox
            value={nameFilter}
            onChange={e => setNameFilter(e.target.value)}
            placeholder={initialSettings.placeholders.nameFilter}
            style={styles.textbox}
          />
          <dc.Textbox
            value={queryPath}
            onChange={e => setQueryPath(e.target.value)}
            placeholder={initialSettings.placeholders.queryPath}
            style={styles.textbox}
          />
        </div>
      </div>

      <DataTable
        columns={columns}
        data={paginatedData}
        columnFilters={columnFilters}
        setColumnFilter={setColumnFilter}
      />

      {initialSettings.pagination.isEnabled && filteredData.length > initialSettings.pagination.itemsPerPage && (
        <Pagination
          currentPage={currentPage}
          totalPages={totalPages}
          setCurrentPage={setCurrentPage}
        />
      )}
    </div>
  );
}

return View;