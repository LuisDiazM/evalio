import styles from './navbar.module.scss';
import { Link } from 'react-router-dom';

const NavBar = () => {
  return (
    <nav>
      <span className={styles.logoContainer}>
        <span className={styles.logoFont}>▮</span> Evalio
      </span>
      <div style={{ marginLeft: 24 }}>
        <Link to="/groups">Grupos</Link>
      </div>
    </nav>
  );
};

export default NavBar;
