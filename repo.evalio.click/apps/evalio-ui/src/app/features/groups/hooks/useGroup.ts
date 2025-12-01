import { useQuery } from '@tanstack/react-query';
import { fetchGroupById } from '@/features/groups/services/groups.service';

export default function useGroup(id?: string) {
  return useQuery({
    queryKey: ['group', id],
    queryFn: () => fetchGroupById(String(id)),
    enabled: Boolean(id),
    staleTime: 1000 * 60 * 2,
  });
}
