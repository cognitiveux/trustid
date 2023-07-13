//
//  StudentLiveExaminationView.swift
//  TrustId
//
//  Created by Adamos Adamou on 14/12/21.
//

import SwiftUI

struct StudentLiveExaminationView: View {
    
    @State var showExam:Bool = false
    
    public let exam_id:String
    
    var body:some View{
        showExam
            ? AnyView(examinationView)
            : AnyView(identificationView)
    }
    
    var identificationView:some View{
        StudentIdentificationSubPageView {
            showExam.toggle()
        }
        .environmentObject(StudentIdentificationSubPageViewModel(exam_id: self.exam_id))
        .environmentObject(VideoPreviewViewModel())
    }

    var examinationView:some View {
        StudentLiveExaminationSubPageView(
            viewModel: .init(exam_id: self.exam_id)
        )
        .environmentObject(VideoPreviewViewModel())
    }
}

struct StudentLiveExaminationView_Previews: PreviewProvider {
    static var previews: some View {
        StudentLiveExaminationView(exam_id: "test_exam_id")
    }
}
