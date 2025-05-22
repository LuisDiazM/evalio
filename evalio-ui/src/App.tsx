import './App.css';
import ListGroup from './components/groups/listGroup/ListGroup';
import Group from './components/groups/listGroup/viewGroup/Group';

import { createBrowserRouter, RouterProvider } from 'react-router';
import ListTemplates from './components/templates/listTemplates/ListTemplates';
import TemplateView from './components/templates/templateview/Template';
import TemplateForm from './components/templates/templateForm/TemplateForm';
import QualificationView from './components/qualifications/qualification/Qualification';
import UploadEvaluation from './components/evaluations/uploadeval/UploadEvaluation';
const router = createBrowserRouter([
  { path: '/', element: <ListGroup></ListGroup>, index: true },
  {
    path: '/groups',
    element: <ListGroup></ListGroup>,
  },
  { path: '/group/:id', element: <Group></Group> },
  { path: '/group/:id/templates', element: <ListTemplates></ListTemplates> },
  { path: '/template/group/:groupId', element: <TemplateForm></TemplateForm> },
  { path: '/template/:id', element: <TemplateView></TemplateView> },
  {
    path: '/qualification/template/:id',
    element: <QualificationView></QualificationView>,
  },
  { path: '/evaluation', element: <UploadEvaluation></UploadEvaluation> },
]);
function App() {
  return (
    <>
      <main>
        <RouterProvider router={router} />
      </main>
    </>
  );
}

export default App;
