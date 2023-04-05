import pandas as pd
from sklearn.neighbors import NearestNeighbors

from sdu.main.models import Profile, Projects


def profile_to_df(profile):
    projects = Projects.objects.filter(participants=profile.id)
    curr_user_dict = {"profile_id": [], "project_id": [], "course_id": []}
    for i in projects:
        curr_user_dict["profile_id"].append(profile.id)
        curr_user_dict["project_id"].append(i.id)
        curr_user_dict["course_id"].append(i.course_id)
    df = pd.DataFrame(curr_user_dict, index=[0])
    return df


def recommendation(profile):
    curr_user_df = profile_to_df(profile)
    all_projects = list(Projects.objects.all())
    projects_dict = {"profile_id": [], "project_id": [], "course_id": []}
    for i in all_projects:
        for j in i.get_participants():
            projects_dict["profile_id"].append(j)
            projects_dict["project_id"].append(i.id)
            projects_dict["course_id"].append(i.course_id)
    df = pd.DataFrame(projects_dict)
    df.drop(df[df.profile_id == profile.id].index, inplace=True)

    X = df.loc[:, ["project_id", "course_id"]]
    knn = NearestNeighbors(
        n_neighbors=len(list(Profile.objects.all())) - 1, algorithm="brute"
    )
    knn.fit(X)
    distances, indices = knn.kneighbors(
        curr_user_df.loc[:, ["project_id", "course_id"]]
    )
    recommendations_list = []

    for i in range(len(distances.flatten())):
        recommendations_list.append(df["profile_id"].iloc[indices.flatten()[i]])

    recommended_profiles = Profile.objects.filter(id__in=recommendations_list)
    return recommended_profiles
