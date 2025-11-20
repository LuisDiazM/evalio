// Uncomment this line to use CSS modules
// import styles from './app.module.scss';

import { Route, Routes } from 'react-router-dom';
import Login from '@/features/login/components/login/Login';
import Signup from '@/features/login/components/signup/Signup';
import NavBar from '@/shared/navBar/NavBar';
import ListGroupPage from '@/features/groups/pages/listGroupPage/ListGroupPage';
import CreateGroup from '@/features/groups/pages/createGroup/CreateGroup';
import GroupDetailPage from './features/groups/pages/groupDetail/GroupDetailPage';
import TemplateDetail from './features/groups/pages/templateView/TemplateDetail';

export function App() {
  return (
    <>
      <NavBar />
      <Routes>
        <Route path="/" element={<Login />} />
        <Route path="/login" element={<Login />} />
        <Route path="/signup" element={<Signup />} />
        <Route path="/groups" element={<ListGroupPage />} />
        <Route path="/group/create" element={<CreateGroup />} />
        <Route path="/group/:id" element={<GroupDetailPage />} />
        <Route path='/group/:groupId/template/:id' element={<TemplateDetail />} />
      </Routes>
    </>
  );
}

export default App;
