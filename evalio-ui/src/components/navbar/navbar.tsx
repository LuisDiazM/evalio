import { Link } from 'react-router';
import './navbar.css';

const Navbar = () => {
  return (
    <>
      <nav>
        <h2>Evalio</h2>
        <span>
          <Link to='/groups'>Grupos</Link>
        </span>
      </nav>
    </>
  );
};

export default Navbar;
