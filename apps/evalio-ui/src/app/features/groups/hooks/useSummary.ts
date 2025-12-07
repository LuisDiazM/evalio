import { useQuery } from '@tanstack/react-query';
import { fetchSummaryByTemplate, TemplateSummary } from '@/features/groups/services/groups.service';

const useSummary = (templateId?: string | null) => {
  return useQuery<TemplateSummary, Error>({
    queryKey: ['summary', templateId],
    queryFn: async () => {
      if (!templateId) throw new Error('templateId is required');
      return fetchSummaryByTemplate(templateId);
    },
    enabled: !!templateId,
  });
};

export default useSummary;
