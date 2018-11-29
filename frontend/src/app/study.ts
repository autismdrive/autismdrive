
export interface Study {
  id: number;
  title: string;
  type: string;
  description: string;
  researcherDescription: string;
  participantDescription: string;
  outcomes: string;
  enrollmentDate: string;
  currentEnrolled: number;
  totalParticipants: number;
  studyDates: string;
  categories: string[];
  status?: string;
}
