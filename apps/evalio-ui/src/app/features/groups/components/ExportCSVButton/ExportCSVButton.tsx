import React, { useState } from 'react';
import api from '@/shared/services/api';
import styles from './exportCsvButton.module.scss';

type Props = {
  templateId: string;
  label?: string;
};

const ExportCSVButton: React.FC<Props> = ({ templateId, label = 'Exportar CSV' }) => {
  const [loading, setLoading] = useState(false);
  const handleExport = async () => {
    setLoading(true);
    try {
      const resp = await api.get(`/manager/summary/export`, {
        params: { template_id: templateId },
        responseType: 'blob',
      });

      const blob = new Blob([resp.data], { type: 'text/csv;charset=utf-8;' });
      const url = window.URL.createObjectURL(blob);
      const a = document.createElement('a');
      a.href = url;
      const filename = `summary-${templateId}.csv`;
      a.setAttribute('download', filename);
      document.body.appendChild(a);
      a.click();
      a.remove();
      window.URL.revokeObjectURL(url);
    } catch (err) {
      console.error('Export CSV error', err);
      // optional: surface UI error
    } finally {
      setLoading(false);
    }
  };

  return (
    <button className={styles.button} onClick={handleExport} disabled={loading} aria-label={label}>
      {loading ? 'Exportando...' : label}
    </button>
  );
};

export default ExportCSVButton;
