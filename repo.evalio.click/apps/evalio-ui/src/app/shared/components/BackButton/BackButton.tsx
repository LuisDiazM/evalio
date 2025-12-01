import React from 'react';
import styles from './backButton.module.scss';

type Props = {
  to?: string;
  onClick?: () => void;
  ariaLabel?: string;
};

const BackButton: React.FC<Props> = ({ to, onClick, ariaLabel = 'Volver' }) => {
  const handleClick = (e: React.MouseEvent) => {
    if (onClick) onClick();
  };

  if (to) {
    // Keep this simple: render a button that callers can wire navigation to via onClick,
    // we prefer keeping routing logic in parent to avoid coupling to react-router here.
  }

  return (
    <button type="button" aria-label={ariaLabel} className={styles.backBtn} onClick={handleClick}>
      <svg width="16" height="16" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg" aria-hidden="true" focusable="false">
        <polyline points="15 18 9 12 15 6" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round" />
      </svg>
    </button>
  );
};

export default BackButton;
