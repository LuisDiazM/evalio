// Uncomment this line to use CSS modules
// import styles from './app.module.scss';

import { Route, Routes } from 'react-router-dom';
import Login from '@/features/login/components/login/Login';
import Signup from '@/features/login/components/signup/Signup';
import NavBar from '@/shared/components/navBar/NavBar';
import ListGroupPage from '@/features/groups/pages/listGroupPage/ListGroupPage';
import CreateGroup from '@/features/groups/pages/createGroup/CreateGroup';
import GroupDetailPage from '@/features/groups/pages/groupDetail/GroupDetailPage';
import TemplateDetail from '@/features/groups/pages/templateView/TemplateDetail';
import UploadExamPage from '@/features/exam/pages/uploadExam/UploadExamPage';
import ProfilePage from '@/features/profile/pages/profilePage/ProfilePage';
import RequireAuth from '@/shared/components/RequireAuth/RequireAuth';

export function App() {
  return (
    <>
      <NavBar />
      <Routes>
        {/* Public routes */}
        <Route path="/" element={<Login />} />
        <Route path="/login" element={<Login />} />
        <Route path="/signup" element={<Signup />} />

        {/* Protected routes: wrap them so only authenticated users (verified with backend) can access */}
        <Route
          path="/groups"
          element={
            <RequireAuth>
              <ListGroupPage />
            </RequireAuth>
          }
        />
        <Route
          path="/group/create"
          element={
            <RequireAuth>
              <CreateGroup />
            </RequireAuth>
          }
        />
        <Route
          path="/group/:id"
          element={
            <RequireAuth>
              <GroupDetailPage />
            </RequireAuth>
          }
        />
        <Route
          path="/group/:groupId/template/:id"
          element={
            <RequireAuth>
              <TemplateDetail />
            </RequireAuth>
          }
        />
        <Route
          path="/exam/upload"
          element={
            <RequireAuth>
              <UploadExamPage />
            </RequireAuth>
          }
        />
        <Route
          path="/profile"
          element={
            <RequireAuth>
              <ProfilePage />
            </RequireAuth>
          }
        />
      </Routes>
    </>
  );
}

export default App;
