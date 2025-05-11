import './App.css';
import ListGroup from './components/groups/listGroup/ListGroup';
import Group from './components/groups/listGroup/viewGroup/Group';

import { createBrowserRouter, RouterProvider } from 'react-router';
import ListTemplates from './components/templates/listTemplates/ListTemplates';
import Template from './components/templates/templateview/Template';
const router = createBrowserRouter([
  { path: '/', element: <ListGroup></ListGroup>, index: true },
  {
    path: '/groups',
    element: <ListGroup></ListGroup>,
  },
  { path: '/group/:id', element: <Group></Group> },
  { path: '/group/:id/templates', element: <ListTemplates></ListTemplates> },
  { path: '/templates', element: <ListTemplates></ListTemplates> },
  { path: '/template/:id', element: <Template></Template> },
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
