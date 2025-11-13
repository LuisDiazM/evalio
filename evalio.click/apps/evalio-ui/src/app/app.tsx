// Uncomment this line to use CSS modules
// import styles from './app.module.scss';

import { Route, Routes } from 'react-router-dom';
import Login from '@/features/login/components/login/Login';
import Signup from '@/features/login/components/signup/Signup';
import NavBar from '@/shared/navBar/NavBar';

export function App() {
  return (
    <>
      <NavBar />
      <Routes>
        <Route path="/" element={<Login />} />
        <Route path="/login" element={<Login />} />
        <Route path="/signup" element={<Signup />} />
      </Routes>
    </>
  );
}

export default App;
