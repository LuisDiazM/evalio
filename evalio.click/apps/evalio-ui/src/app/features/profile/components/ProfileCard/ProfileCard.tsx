import React from 'react';
import styles from './profileCard.module.scss';
import { useUser } from '@/shared/context/UserContext';

const ProfileCard: React.FC = () => {
  const { user } = useUser();

  if (!user) {
    return <div className={styles.container}>No hay información de usuario</div>;
  }

  return (
    <div className={styles.card}>
      <div className={styles.header}>
        <div className={styles.avatar} aria-hidden>
          {user.name?.charAt(0) ?? 'U'}
        </div>
        <div className={styles.titleGroup}>
          <div className={styles.name}>{user.name}</div>
          <div className={styles.role}>Profesor</div>
        </div>
      </div>

      <div className={styles.content}>
        <div className={styles.row}>
          <div className={styles.label}>Email</div>
          <div className={styles.value}>{user.email}</div>
        </div>
        <div className={styles.row}>
          <div className={styles.label}>ID Profesor</div>
          <div className={styles.value}>{user.professor_id ?? '-'}</div>
        </div>
      </div>
    </div>
  );
};

export default ProfileCard;
