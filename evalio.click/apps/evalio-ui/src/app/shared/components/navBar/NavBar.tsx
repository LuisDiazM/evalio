import styles from './navbar.module.scss';
import { Link } from 'react-router-dom';
import { useUser } from '@/shared/context/UserContext';
import { useNavigate } from 'react-router-dom';

const NavBar = () => {
  const { user, logout } = useUser();
  const navigate = useNavigate();

  const handleLogout = () => {
    try {
      logout();
    } finally {
      navigate('/login');
    }
  };

  return (
    <nav className={styles.nav}>
      <div className={styles.left}>
        <span className={styles.logoContainer}>
          <span className={styles.logoFont}>▮</span> Evalio
        </span>

        {user ? (
          <div className={styles.links}>
            <Link to="/groups">Grupos</Link>
            <Link to="/exam/upload">Subir Examen</Link>
          </div>
        ) : null}
      </div>

      {user ? (
        <div className={styles.avatarContainer}>
          <Link to="/profile" title="Perfil">
            <div className={styles.avatar} aria-hidden>
              {/* simple user svg */}
              <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="1.5" strokeLinecap="round" strokeLinejoin="round" xmlns="http://www.w3.org/2000/svg">
                <path d="M20 21v-2a4 4 0 0 0-4-4H8a4 4 0 0 0-4 4v2"></path>
                <circle cx="12" cy="7" r="4"></circle>
              </svg>
            </div>
          </Link>
          <button onClick={handleLogout} className={styles.logout} aria-label="Salir">
            Salir
          </button>
        </div>
      ) : null}
    </nav>
  );
};

export default NavBar;
