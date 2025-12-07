import { useQuery } from '@tanstack/react-query';
import { fetchGroups, Group } from '@/features/groups/services/groups.service';

const QUERY_KEY = ['groups'];

export default function useGroups() {
  return useQuery<Group[], Error>({
    queryKey: QUERY_KEY,
    queryFn: fetchGroups,
    staleTime: 1000 * 60 * 2, // 2 minutes
    retry: 1,
  });
}
