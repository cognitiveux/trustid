//
//  UserFeedbackView.swift
//  TrustId
//
//  Created by Adamos Adamou on 23/1/22.
//

import SwiftUI

struct UserFeedbackView: View {
    
    @StateObject public var viewModel:UserFeedbackViewModel
    
    var body: some View {
        VStack(alignment:.leading, spacing:32){
            Text("User Feedback Mechanism")
                .font(.custom("Roboto", size: 13))
                .bold()
            
            VStack(alignment:.leading, spacing: 8){
                HStack(spacing: 16){
                    CheckBoxView(checked: $viewModel.checkedImpersonationBox)
                    Text("I will impersonate with another person")
                        .font(.custom("Roboto", size: 13))
                    Spacer()
                }
                
                HStack(spacing: 16){
                    CheckBoxView(checked: $viewModel.checkedApplicationBox)
                    Text("I will open a forbidden application")
                        .font(.custom("Roboto", size: 13))
                    Spacer()
                }
            }
            
            VStack(alignment:.leading, spacing: 4){
                PlaceHolderTextEditor(
                    placeholder: "Comment, e.g., I opened Skype",
                    text: $viewModel.feedbackText
                )
                .border(TrustIdPalette.lightGray, width: 1)
                    
                Text(viewModel.instructionText)
                    .font(.custom("Roboto", size: 11))
                    .italic()
                
                Text(viewModel.errorText)
                    .font(.custom("Roboto", size: 11))
                    .italic()
                    .foregroundColor(TrustIdPalette.red)
                
            }
            
            HStack{
                Spacer()
                Button("Send Feedback") {
                    viewModel.sendFeeback()
                }
                .font(.custom("Roboto", size: 13))
                .buttonStyle(BlueButton())
                Spacer()
            }
        }
        .background(Color.white)
        .padding()
        .overlay(LoadingView(isLoading: viewModel.isLoading))
    }
}

struct PlaceHolderTextEditor: View {
    let placeholder: String
    @Binding var text: String
    
    @State var isFocused = false
    
    var body: some View {
        ZStack(alignment: Alignment(horizontal: .leading, vertical: .top)) {
            if text.isEmpty {
                Text(placeholder)
                    .font(.custom("Roboto", size: 13))
                    .foregroundColor(.black)
                    .italic()
                    .padding(.horizontal, 4)
            }
            TextEditor(text: $text)
                .font(.custom("Roboto", size: 13))
                .opacity(text.isEmpty ? 0.7 : 1)
        }
        .padding(8)
        .overlay(
            RoundedRectangle(cornerRadius: 6)
                .stroke(TrustIdPalette.lightGray, lineWidth: 1.0)
        )
        .frame(height:88)
    }
}

struct CheckBoxView: View {
    @Binding var checked: Bool
    
    var body: some View {
        Image(systemName: imageName)
            .foregroundColor(TrustIdPalette.buttonBlue)
            .onTapGesture {
                self.checked.toggle()
            }
    }

    private var imageName:String{
        checked ? "checkmark.square.fill" : "square"
    }
}

struct UserFeedbackView_Previews: PreviewProvider {
    static var previews: some View {
        UserFeedbackView(viewModel: .init(exam_id: "-"))
    }
}
