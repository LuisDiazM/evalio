import React from 'react';
import styles from './deleteTemplate.module.scss';
import { useMutation, useQueryClient } from '@tanstack/react-query';
import { deleteTemplate } from '@/features/groups/services/groups.service';
import DeleteIcon from '@/shared/components/deleteIcon/deleteIcon';

type Props = { templateId: string };

const DeleteTemplateButton: React.FC<Props> = ({ templateId }) => {
  const qc = useQueryClient();
  const mutation = useMutation({
    mutationFn: (id: string) => deleteTemplate(id),
    onSuccess: () => {
      qc.invalidateQueries({ queryKey: ['templates'] });
    },
  });

  const handleDelete = async () => {
    const ok = window.confirm(
      '¿Eliminar esta plantilla? Esta acción no se puede deshacer.'
    );
    if (!ok) return;
    try {
      await mutation.mutateAsync(templateId);
    } catch (err) {
      console.error(err);
      alert('No se pudo eliminar la plantilla');
    }
  };

  const loading =
    String((mutation as unknown as { status?: string }).status) === 'pending';

  return (
    <button
      className={styles.btn}
      onClick={(e) => {
        e.stopPropagation();
        handleDelete();
      }}
      disabled={loading}
      aria-label="Eliminar plantilla"
    >
      <DeleteIcon></DeleteIcon>
    </button>
  );
};

export default DeleteTemplateButton;
