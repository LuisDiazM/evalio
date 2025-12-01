import React from 'react';
import styles from './deleteGroup.module.scss';
import { useMutation, useQueryClient } from '@tanstack/react-query';
import { deleteGroup } from '@/features/groups/services/groups.service';
import DeleteIcon from '@/shared/components/deleteIcon/deleteIcon';

type Props = { groupId: string };

const DeleteGroupButton: React.FC<Props> = ({ groupId }) => {
  const qc = useQueryClient();
  const mutation = useMutation({
    mutationFn: (id: string) => deleteGroup(id),
    onSuccess: () => {
      qc.invalidateQueries({ queryKey: ['groups'] });
    },
  });

  const handleDelete = async () => {
    const ok = window.confirm('¿Eliminar este grupo? Esta acción no se puede deshacer.');
    if (!ok) return;
    try {
      await mutation.mutateAsync(groupId);
    } catch (err) {
      console.error(err);
    }
  };

  const loading = String((mutation as unknown as { status?: string }).status) === 'pending';

  return (
    <button className={styles.btn} onClick={handleDelete} disabled={loading} aria-label="Eliminar grupo">
      <DeleteIcon></DeleteIcon>
    </button>
  );
};

export default DeleteGroupButton;
