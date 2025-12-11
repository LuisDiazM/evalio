import React, { useEffect, useRef, useState } from 'react';
import styles from './qualificationsList.module.scss';

type Props = {
  src: string;
  alt?: string;
  onClose: () => void;
};

const ModalImageViewer: React.FC<Props> = ({ src, alt = 'Examen', onClose }) => {
  const [isLoading, setIsLoading] = useState(true);
  const closeBtnRef = useRef<HTMLButtonElement | null>(null);
  const modalRef = useRef<HTMLDivElement | null>(null);
  const lastFocusedRef = useRef<HTMLElement | null>(null);

  useEffect(() => {
    // save previously focused element
    lastFocusedRef.current = document.activeElement as HTMLElement | null;
    // focus the close button when opened
    setTimeout(() => closeBtnRef.current?.focus(), 0);

    function onKey(e: KeyboardEvent) {
      if (e.key === 'Escape') {
        onClose();
        return;
      }

      if (e.key === 'Tab' && modalRef.current) {
        const focusable = modalRef.current.querySelectorAll<HTMLElement>(
          'button, [href], input, select, textarea, [tabindex]:not([tabindex="-1"])'
        );
        if (focusable.length === 0) return;
        const first = focusable[0];
        const last = focusable[focusable.length - 1];
        if (e.shiftKey && document.activeElement === first) {
          e.preventDefault();
          last.focus();
        } else if (!e.shiftKey && document.activeElement === last) {
          e.preventDefault();
          first.focus();
        }
      }
    }

    document.addEventListener('keydown', onKey);
    return () => {
      document.removeEventListener('keydown', onKey);
      // restore focus
      try {
        lastFocusedRef.current?.focus();
      } catch {
        // ignore
      }
    };
  }, [onClose]);

  return (
    <div role="dialog" aria-modal="true" className={styles.modalOverlay} onClick={onClose}>
      <div className={styles.modalContent} onClick={(e) => e.stopPropagation()}>
        <button aria-label="Cerrar" className={styles.closeBtn} onClick={onClose} ref={closeBtnRef}>
          ×
        </button>
        <div ref={modalRef} className={styles.modalInner}>
          {isLoading && <div className={styles.spinner} aria-hidden="true" />}
          <img
            src={src}
            alt={alt}
            className={styles.previewImage}
            onLoad={() => setIsLoading(false)}
            onError={() => setIsLoading(false)}
            style={{ display: isLoading ? 'none' : 'block' }}
          />
        </div>
      </div>
    </div>
  );
};

export default ModalImageViewer;
