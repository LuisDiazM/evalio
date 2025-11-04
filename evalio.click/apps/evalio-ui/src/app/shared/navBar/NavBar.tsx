import styles from './navbar.module.scss';
const NavBar = () => {
  return (
    <nav>
      <span className={styles.logoContainer}>
        <span className={styles.logoFont}>▮</span> Evalio
      </span>
    </nav>
  );
};

export default NavBar;
