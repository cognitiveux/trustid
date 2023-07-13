//
//  StudentActionToolbar.swift
//  TrustId
//
//  Created by Adamos Adamou on 29/11/21.
//

import SwiftUI

struct StudentActionToolbar: View {
    public var actions: [StudentExaminationAction]
    public var selectedAction:Binding<StudentExaminationAction?>
    public var didSelect: (StudentExaminationAction)->Void
    
    var body: some View {
        HStack{
            Button(StudentExaminationAction.join.rawValue){
                didSelect(.join)
            }
            .font(.custom("Roboto", size: 13))
            .buttonStyle(BlueButton())
            Spacer()
            ForEach(subpageActions){ action in
                Button(action.rawValue){
                    didSelect(action)
                }
                .font(.custom("Roboto", size: 13))
                .buttonStyle(WhiteButton(isSelected: isSelected(action)))
            }
            Spacer()
        }
    }
    
    private var subpageActions: [StudentExaminationAction]{
        guard actions.count > 0 else { return [] }
        return actions.filter{ $0 != .join }
    }
    
    private func isSelected(_ action:StudentExaminationAction) -> Bool{
        return action.rawValue == selectedAction.wrappedValue?.rawValue ?? "-"
    }
}

struct StudentActionToolbar_Previews: PreviewProvider {
    
    static var actions = StudentExaminationAction.allCases
    static var selectedAction:Binding<StudentExaminationAction?> = .constant(.information)
    
    static var previews: some View {
        StudentActionToolbar(actions: actions, selectedAction: selectedAction){ action in
            print("action \(action.rawValue)")
        }
    }
}
