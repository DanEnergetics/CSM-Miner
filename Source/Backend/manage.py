#!/usr/bin/env python
"""Django's command-line utility for administrative tasks."""
import os
import sys
from View.ViewSet import ViewSet
from View.viewItem import viewItem


def main():
    view = ViewSet()
    container = viewItem("ALL")
    graph = viewItem("GraphA")
    knotenA = viewItem("KnotenA")
    indir = viewItem("DirekteKnoten")
    knotenB = viewItem("KnotenB")
    chanceB = viewItem("chance","0.5")
    knotenC = viewItem("KnotenC")
    chanceC = viewItem("chance","0.5")
    knotenC.addChild(chanceC)
    indir.addChild(knotenC)
    knotenB.addChild(chanceB)
    indir.addChild(knotenB)
    knotenA.addChild(indir)
    graph.addChild(knotenA)
    container.addChild(graph)
    view.setHead(container)
    print(view.toJSON())
    print("-------\n")
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'CSMMiner.settings')
    try:
        from django.core.management import execute_from_command_line
    except ImportError as exc:
        raise ImportError(
            "Couldn't import Django. Are you sure it's installed and "
            "available on your PYTHONPATH environment variable? Did you "
            "forget to activate a virtual environment?"
        ) from exc
    execute_from_command_line(sys.argv)


if __name__ == '__main__':
    main()
