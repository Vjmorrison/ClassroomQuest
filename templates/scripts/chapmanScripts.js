/**
 * Created with PyCharm.
 * User: vjmor_000
 * Date: 8/24/13
 * Time: 6:12 PM
 * To change this template use File | Settings | File Templates.
 */



function OnSaveChanges()
{
    var saveBTN = document.getElementById("saveChangesBTN");
    saveBTN.className = "btn btn-warning";
    saveBTN.innerHTML = "Saving...";
    saveBTN.disabled = true;

    var newSelect = document.getElementById("selectedProject");
    var selectedKey = newSelect.options[newSelect.selectedIndex].value;
    $.ajax(
        {
            type:"POST",
            data: "currentProjectKey=" + selectedKey.toString(),
            cache: false,
            url: "/charactersheet",
            success: OnRequestSuccess
        }
    );
}

function OnSubmitProject()
{
    var saveBTN = document.getElementById("submitBTN");
    saveBTN.className = "btn btn-warning";
    saveBTN.innerHTML = "Submitting...";
    saveBTN.disabled = true;

    var saveBTN = document.getElementById("saveChangesBTN");
    if(!saveBTN.disabled)
    {
        OnSaveChanges();
    }
    var selectedKey = GetSelectedProjectID();
    $.ajax(
        {
            type:"POST",
            data: "currentProjectKey=" + selectedKey.toString() + "&SubmitProject=True",
            cache: false,
            url: "/charactersheet",
            success: OnSubmitSuccess
        }
    );
}

function OnSubmitSuccess(response, status, jqXHR)
{
    var saveBTN = document.getElementById("submitBTN");
    saveBTN.className = "btn btn-inverse";
    saveBTN.innerHTML = "Submitted";
    saveBTN.disabled = true;

    var dropdownBTN = document.getElementById("selectedProject");
    dropdownBTN.disabled = true;

    var submitContainer = document.getElementById("submitContainer");
    submitContainer.innerHTML = '<p><span class="badge badge-important">!</span>You have already submitted a project!  Please wait for the instructor to review the project. please be prepared to have your project available to show at the next possible class.</p><p>Feel free to work on additional projects before then.</p>'
}

function GetSelectedProjectID()
{
    var newSelect = document.getElementById("selectedProject");
    var selectedKey = newSelect.options[newSelect.selectedIndex].value;

    return selectedKey;
}

function OnRequestSuccess(response, status, jqXHR)
{
    console.log(response);
    var saveBTN = document.getElementById("saveChangesBTN");
    saveBTN.className = "btn btn-inverse";
    saveBTN.innerHTML = "Saved";
    saveBTN.disabled = true;

    var submitBTN = document.getElementById("submitBTN");
    submitBTN.disabled = false;
    submitBTN.className = "btn btn-danger";
    submitBTN.innerHTML = "Submit Project";
}

function OnUnsavedChanges()
{
    var saveBTN = document.getElementById("saveChangesBTN");
    saveBTN.disabled = false;
    saveBTN.className = "btn btn-success";
    saveBTN.innerHTML = "Save Changes";
    ToggleProjectVisible(GetSelectedProjectID());
}


function OnAcceptProject(SubKey, userID)
{
    console.log(userID)
    var AcceptBTN = document.getElementById("Accept"+SubKey);
    var RejectBTN = document.getElementById("Reject"+SubKey);
    AcceptBTN.disabled = true;
    RejectBTN.parentNode.removeChild(RejectBTN);

    $.ajax(
        {
            type:"POST",
            data: "submissionKey=" + SubKey +"&Accept=True" + "&userID=" + userID,
            cache: false,
            url: "/admin",
            success: function(response) {
                OnAcceptSuccess(response, SubKey);
            }
        }
    );
}

function OnAcceptSuccess(response, submissionID)
{
    var row = document.getElementById(submissionID)
    row.disabled = true;
}

function OnRejectProject(SubKey, userID)
{
    var AcceptBTN = document.getElementById("Accept"+SubKey);
    var RejectBTN = document.getElementById("Reject"+SubKey);
    RejectBTN.disabled = true;
    AcceptBTN.parentNode.removeChild(AcceptBTN);

    $.ajax(
        {
            type:"POST",
            data: "submissionKey=" + SubKey + "&userID=" + userID,
            cache: false,
            url: "/admin",
            success: function(response) {
                OnRejectSuccess(response, SubKey);
            }
        }
    );
}

function OnRejectSuccess(response, submissionID)
{
    var row = document.getElementById(submissionID)
    row.disabled = true;
}

function InitSelectedProject(selectedKey)
{
    if(selectedKey == 0)
    {
        selectedKey = GetSelectedProjectID()
    }
    window.selectedKey = selectedKey;
    ToggleProjectVisible(selectedKey);
}

function InitRequirements()
{
    window.requirementsCount = $("#requirementsList li").size() - 1
}

function ToggleProjectVisible(projectKey)
{
    var selectedProjectInfo = document.getElementById("info_" + projectKey);
    if(selectedProjectInfo != null)
    {
        if(selectedProjectInfo.classList.contains("hide"))
        {
            selectedProjectInfo.classList.remove("hide");
            var selectedVideoDiv = document.getElementById("video_" + projectKey);
            if(selectedVideoDiv != null)
            {
                var selectedVideoURL = document.getElementById("videoURL_" + projectKey).textContent;
                if(selectedVideoURL != "None" && selectedVideoURL != "")
                {
                    selectedVideoDiv.innerHTML = '<iframe width="420" height="315" src="//www.youtube.com/embed/' + selectedVideoURL + '?rel=0" frameborder="0" allowfullscreen></iframe>';
                }
            }

        }

        if(window.selectedKey != projectKey)
        {
            var windowProjectInfo = document.getElementById("info_"+window.selectedKey);
            if(!windowProjectInfo.classList.contains("hide"))
            {
                windowProjectInfo.classList.add("hide");
                var selectedVideoDiv = document.getElementById("video_" + window.selectedKey);
                if(selectedVideoDiv != null)
                {
                    var selectedVideoURL = document.getElementById("videoURL_" + window.selectedKey).textContent;
                    selectedVideoDiv.innerHTML = "";
                }
            }

            window.selectedKey = projectKey;
        }
    }
}

function ToggleProjectDetails(ButtonID, parentID)
{
    var moreInfoBTN = document.getElementById(ButtonID);
    var parentObj = document.getElementById(parentID);
    if(parentObj != null && parentObj.classList.contains("hide"))
    {
        moreInfoBTN.innerHTML = "Hide Project Info";
        moreInfoBTN.classList.remove("btn-info");
        moreInfoBTN.classList.add("btn-inverse");
        parentObj.classList.remove("hide");
    }
    else if (parentObj != null)
    {
        moreInfoBTN.innerHTML = "Show Project Info";
        moreInfoBTN.classList.add("btn-info");
        moreInfoBTN.classList.remove("btn-inverse");
        parentObj.classList.add("hide");
    }
}

function AddRequirement()
{
    if(window.requirementsCount == null)
    {
        InitRequirements();
    }
    window.requirementsCount++;
    var list = document.getElementById("requirementsList");

    var newReq = document.createElement("li");
    var newInput = document.createElement("input");

    newInput.id = "requirement_" + window.requirementsCount;
    newInput.name = "requirement_" + window.requirementsCount;
    newInput.type = "text";
    newInput.className = "input-xxlarge";

    newReq.appendChild(newInput);
    list.appendChild(newReq);
}

function RemoveRequirement()
{
    if(window.requirementsCount == null)
    {
        InitRequirements();
    }

    var list = document.getElementById("requirementsList");
    var newInput = document.getElementById("requirement_" + window.requirementsCount);

    if(newInput != null)
    {
        list.removeChild(newInput.parentNode)
    }
    window.requirementsCount--;
}