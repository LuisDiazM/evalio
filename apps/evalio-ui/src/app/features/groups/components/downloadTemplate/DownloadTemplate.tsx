import { useMutation } from '@tanstack/react-query';
import { fetchTemplateFile } from '@/features/groups/services/groups.service';
import type { Template } from '@/features/groups/services/groups.service';
import styles from './downloadTemplate.module.scss';

export const DownloadTemplate: React.FC<{ template: Template }> = ({ template }) => {
  const mutation = useMutation({
    mutationFn: async ({ groupId, templateId }: { groupId: string; templateId: string }) => {
      return fetchTemplateFile(groupId, templateId);
    },
  });

  const handleClick = async () => {
    try {
  const blob = await mutation.mutateAsync({ groupId: template.group_id, templateId: (template as any).template_id || template.id });
      const url = URL.createObjectURL(blob);
      window.open(url, '_blank');
      // release the object URL later
      setTimeout(() => URL.revokeObjectURL(url), 10000);
    } catch (err) {
      console.error('Error fetching template file', err);
    }
  };

  const loading = String((mutation as unknown as { status?: string }).status) === 'pending';

  return (
    <button className={styles.downloadBtn} onClick={handleClick} disabled={loading}>
      {loading ? 'Descargando...' : 'Ver / Descargar'}
    </button>
  );
};
