import { useQuery } from '@tanstack/react-query';
import { fetchTemplatesByGroup, Template } from '@/features/groups/services/groups.service';

export default function useTemplatesByGroup(groupId?: string) {
  return useQuery<Template[]>({
    queryKey: ['templates', groupId],
    queryFn: () => fetchTemplatesByGroup(String(groupId)),
    enabled: Boolean(groupId),
  });
}
