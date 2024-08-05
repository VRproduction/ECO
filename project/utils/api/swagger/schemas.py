from drf_spectacular.openapi import AutoSchema

from drf_spectacular.utils import OpenApiParameter


class CustomAutoSchema(AutoSchema):
    global_params = [
        # OpenApiParameter(
        #     name="Accept-Language",
        #     type=str,
        #     location=OpenApiParameter.HEADER,
        #     description="`az` or `en` or `ru`. The default value is az",
        # ),
        OpenApiParameter(
            name='API-KEY',
            description='API key for authorization',
            required=True,
            type=str,
            location=OpenApiParameter.HEADER,
        )
    ]

    def get_override_parameters(self):
        params = super().get_override_parameters()
        return params + self.global_params