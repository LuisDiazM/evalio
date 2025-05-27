import { Link } from 'react-router';
import './navbar.css';

const Navbar = () => {
  return (
    <>
      <header>
        <nav>
          <h2>Evalio</h2>
          <div className='menu'>
            <span>
              <Link to='/groups'>Grupos</Link>
            </span>
            <span>
              <Link to='/evaluation'>Parciales</Link>
            </span>
          </div>
        </nav>
      </header>
    </>
  );
};

export default Navbar;
