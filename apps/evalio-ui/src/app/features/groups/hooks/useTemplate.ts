import { useQuery } from '@tanstack/react-query';
import { fetchTemplateById, Template } from '@/features/groups/services/groups.service';

const useTemplate = (id?: string) => {
  return useQuery<Template>({
    queryKey: ['template', id],
    queryFn: () => fetchTemplateById(id as string),
    enabled: Boolean(id),
    staleTime: 1000 * 60 * 5,
  });
};

export default useTemplate;
