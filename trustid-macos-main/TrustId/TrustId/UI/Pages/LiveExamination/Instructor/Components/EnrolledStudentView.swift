//
//  EnrolledStudentView.swift
//  TrustId
//
//  Created by Adamos Adamou on 23/1/22.
//

import SwiftUI

struct EnrolledStudentView: View {
    
    public let student:InstructorLiveExaminationView.EnrolledStudent
    
    public let didTapApproved:(InstructorLiveExaminationView.EnrolledStudent)->Void
    
    var body: some View {
        ZStack{
            HStack(spacing:16){
                Text(student.initials)
                    .font(.custom("Roboto", size: 13))
                    .padding(8)
                    .background(TrustIdPalette.profileBlue)
                    .foregroundColor(.white)
                    .clipShape(RoundedRectangle.init(cornerRadius: 8))
                
                VStack(alignment:.leading, spacing:4){
                    HStack(spacing:4){
                        Text(student.fullname)
                            .font(.custom("Roboto", size: 13))
                        Text("::")
                            .font(.custom("Roboto", size: 13))
                        Text(student.email)
                            .font(.custom("Roboto", size: 13))
                    }
                    Text(student.status)
                        .font(.custom("Roboto", size: 13))
                        .foregroundColor(getStudentStatusColor(student.status))
                }
                
                Spacer()
                
                if student.status == "Requested Manual Approval"{
                    Button("Approve"){
                        didTapApproved(student)
                    }
                    .font(.custom("Roboto", size: 13))
                    .buttonStyle(BlueButton())
                }
            }
        }
        .padding()
        .background(getCellBackgroundColor(student.status))
    }
    
    private func getCellBackgroundColor(_ status:String) -> Color{
        student.status == "Requested approval"
            ? TrustIdPalette.lightGray
            : .clear
    }
    
    private func getStudentStatusColor(_ status:String) -> Color{
        switch status{
        case "Verified": return TrustIdPalette.green
        case "Requested approval": return TrustIdPalette.red
        case "Pending": return TrustIdPalette.buttonBlue
            
        default: return Color.black
        }
    }
}

struct EnrolledStudentView_Previews: PreviewProvider {
    
    static var student = MockLiveExamService.enrolledStudents.first!
    
    static var previews: some View {
        EnrolledStudentView(student: student, didTapApproved: { _ in })
            .frame(width:400, height:65)
    }
}
