//
//  ExaminationPageView.swift
//  TrustId
//
//  Created by Adamos Adamou on 29/11/21.
//

import SwiftUI

struct ExaminationPageView: View {
    
    var body: some View {
        examinationView
            .background(Color.white)
    }
    
    private var examinationView: some View{
        let userService = UserService.shared
        
        guard let user = userService.retrieveUser() else {
            return AnyView(
                Text("Unauthorized")
                    .font(.custom("Roboto", size: 13))
            )
        }
        
        switch user.type {
        
        case .student:
            return AnyView(StudentExaminationView())
        
        case .instructor:
            return AnyView(InstructorExaminationView())
        }
    }
}

struct ExaminationPageView_Previews: PreviewProvider {
    static var previews: some View {
        ExaminationPageView()
    }
}
