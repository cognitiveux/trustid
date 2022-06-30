//
//  LiveExaminationPageView.swift
//  TrustId
//
//  Created by Adamos Adamou on 30/11/21.
//

import SwiftUI

struct LiveExaminationPageView: View {
    
    public let exam_id:String
    
    var body: some View {
        liveExaminationView
            .background(Color.white)
    }
    
    private var liveExaminationView: some View{
        let userService = UserService.shared
        
        guard let user = userService.retrieveUser() else {
            return AnyView(
                Text("Unauthorized")
                    .font(.custom("Roboto", size: 13))
            )
        }
        
        switch user.type {
        
        case .student:
            return AnyView(StudentLiveExaminationView(exam_id: exam_id))
            
        case .instructor:
            return AnyView(makeInstructorLiveExaminationView(exam_id: exam_id))
        }
    }
    
    private func makeInstructorLiveExaminationView(exam_id:String) -> some View{
        return InstructorLiveExaminationView(
            viewModel: .init(exam_id: exam_id)
        )
    }
}

struct LiveExaminationPageView_Previews: PreviewProvider {
    static var previews: some View {
        LiveExaminationPageView(exam_id: "test_exam_id")
    }
}
