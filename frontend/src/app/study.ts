
export interface Study {
  id: number;
  title: string;
  description: string;
  researcherDescription: string;
  participantDescription: string;
  outcomes: string;
  enrollmentDate: string;
  currentEnrolled: number;
  totalParticipants: number;
  studyStart: string;
  studyEnd: string;
  categories: string[];
  status?: string;
}
