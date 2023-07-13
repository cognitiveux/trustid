//
//  EnrolledStudentsListView.swift
//  TrustId
//
//  Created by Adamos Adamou on 23/1/22.
//

import SwiftUI

struct EnrolledStudentsListView: View {
    
    public let enrolledStudents:[InstructorLiveExaminationView.EnrolledStudent]
    public let filter:String
    public let didTapApproved:(InstructorLiveExaminationView.EnrolledStudent)->Void
    
    var body: some View {
        List(filteredStudents){ student in
            EnrolledStudentView(student: student, didTapApproved: didTapApproved)
                .frame(height: 65)
        }
    }
    
    private var filteredStudents:[InstructorLiveExaminationView.EnrolledStudent]{
        if filter == "All"{
            return enrolledStudents
        }
        
        return enrolledStudents.filter{
            $0.status == filter
        }
    }
}

struct EnrolledStudentsListView_Previews: PreviewProvider {
    
    static var students = MockLiveExamService.enrolledStudents
    static var filter = InstructorLiveExaminationView.EnrolledStudentFilter.all
    
    static var previews: some View {
        EnrolledStudentsListView(
            enrolledStudents: students,
            filter: filter.rawValue,
            didTapApproved: { _ in }
        )
    }
}
