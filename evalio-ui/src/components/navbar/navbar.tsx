import { Link, useNavigate } from 'react-router';
import './navbar.css';

const Navbar = () => {

  const navigate = useNavigate()

  const handleLogout = () => {
    localStorage.removeItem("access_token")
    navigate("/")
  }

  return (
    <>
      <header>

        <nav style={{ height: 60, display: 'flex', alignItems: 'center', padding: '0 24px' }}>
          <span style={{ fontWeight: 700, fontSize: 22, display: 'flex', alignItems: 'center' }}>
            <span style={{ marginRight: 8, fontSize: 24 }}>▮</span> Evalio
          </span>
          <div className='menu'>
            <span>
              <Link to='/groups'>Grupos</Link>
            </span>
            <span>
              <Link to='/evaluation'>Parciales</Link>
            </span>
          </div>
        </nav>
        <span onClick={()=>handleLogout()} id='logout' >
          Salir
        </span>

      </header>
    </>
  );
};

export default Navbar;
