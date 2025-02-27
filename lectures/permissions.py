from rest_framework import permissions


class IsOwnerOrPublicReadOnly(permissions.BasePermission):
    """
    講義に所有者がいる場合、その所有者のみが閲覧・編集・削除を許可。
    所有者がいない場合は、全ユーザーに読み取りを許可。
    """

    def has_object_permission(self, request, view, obj):
        # 安全なメソッド（GET, HEAD, OPTIONS）は許可
        if request.method in permissions.SAFE_METHODS:
            if obj.owner:
                return obj.owner == request.user
            return True

        # 安全でないメソッド（POST, PUT, DELETE）は所有者のみ許可
        if obj.owner:
            return obj.owner == request.user

        # 所有者がいない場合は安全でないメソッドを許可しない
        return False
